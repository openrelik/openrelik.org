# Copyright 2025-2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# /// script
# requires-python = ">= 3.10"
# dependencies = [
#     "requests",
#     "PyYAML",
#     "PyGithub",
# ]
# ///

"""Search GitHub for openrelik.yaml files and generate data/workerhub.yaml."""

import argparse
import logging
import os
import sys
from pathlib import Path

import requests
import yaml
from github import Auth, Github, GithubException

log = logging.getLogger(__name__)


def fetch_yaml_content(url: str) -> dict | None:
    """Download and parse a YAML file from a URL.

    Args:
        url: Direct download URL for the YAML file.

    Returns:
        Parsed YAML content as a dict, or None on failure.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        log.warning("Failed to download %s: %s", url, e)
        return None

    try:
        return yaml.safe_load(response.text)
    except yaml.YAMLError as e:
        log.warning("Failed to parse YAML from %s: %s", url, e)
        return None


def build_item(file, yaml_content: dict) -> dict | None:
    """Extract and normalize metadata for one repository.

    Args:
        file: A GitHub ContentFile search result.
        yaml_content: Parsed openrelik.yaml content.

    Returns:
        A dict of item fields, or None if the item should be skipped.
    """
    if not yaml_content.get("publish", False):
        log.debug("Skipping %s (publish=false)", file.repository.full_name)
        return None

    display_name = yaml_content.get("display_name", "N/A")
    description = yaml_content.get("description", "N/A")

    if display_name.startswith("User-friendly"):
        display_name = file.repository.name

    if description.startswith("A brief description"):
        description = ""

    return {
        "display_name": display_name,
        "description": description,
        "tools": yaml_content.get("tools", []),
        "repository": file.repository.full_name,
        "license": file.repository.license.name if file.repository.license else "N/A",
        "owner": file.repository.owner.name,
        "updated_at": file.repository.updated_at.strftime("%Y-%m-%d"),
        "url": file.repository.html_url,
        "github_stars": file.repository.stargazers_count,
    }


def search_github(github: Github) -> list[dict]:
    """Search GitHub for openrelik.yaml files and return worker items.

    Args:
        github: Authenticated PyGithub instance.

    Returns:
        List of worker item dicts.
    """
    query = "filename:openrelik.yaml in:path language:yaml"
    results = github.search_code(query=query)

    items = []
    for file in results:
        if file.path != "openrelik.yaml":
            continue

        log.debug("Processing %s", file.repository.full_name)

        yaml_content = fetch_yaml_content(file.download_url)
        if yaml_content is None:
            continue

        item = build_item(file, yaml_content)
        if item is not None:
            items.append(item)

    return items


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search GitHub for openrelik.yaml and generate workerhub YAML data.",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN", ""),
        help="GitHub personal access token (default: $GITHUB_TOKEN)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/workerhub.yaml"),
        help="Output file path (default: data/workerhub.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print YAML to stdout instead of writing to file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if not args.token:
        log.error("GitHub token required. Set GITHUB_TOKEN or pass --token.")
        return 1

    try:
        github = Github(auth=Auth.Token(args.token))
        github.get_user().login  # verify auth
    except GithubException as e:
        log.error("GitHub authentication failed: %s", e)
        return 1

    log.info("Searching GitHub for openrelik.yaml files...")
    items = search_github(github)
    log.info("Found %d published items", len(items))

    output_yaml = yaml.dump({"items": items}, sort_keys=False)

    if args.dry_run:
        print(output_yaml)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_yaml)
        log.info("Wrote %s", args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
