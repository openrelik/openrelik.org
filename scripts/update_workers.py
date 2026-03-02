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

"""Search GitHub for openrelik.yaml files and generate data/workerhub.json."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import requests
import yaml
from github import Auth, Github, GithubException

log = logging.getLogger(__name__)

unpublished_workers = set()


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
        unpublished_workers.add(file.repository.full_name)
        return None

    display_name = yaml_content.get("display_name", "N/A")
    description = yaml_content.get("description", "N/A")

    if display_name.startswith("User-friendly"):
        display_name = file.repository.name

    if description.startswith("A brief description"):
        description = ""

    repo_url = file.repository.html_url
    repo_display_name = file.repository.full_name

    if file.path != "openrelik.yaml":
        folder_path = os.path.dirname(file.path)
        repo_url = f"{repo_url}/tree/main/{folder_path}"
        repo_display_name = f"{repo_display_name}/{folder_path}"

    return {
        "display_name": display_name,
        "description": description,
        "tools": yaml_content.get("tools", []),
        "repository": repo_display_name,
        "license": file.repository.license.name if file.repository.license else "N/A",
        "owner": file.repository.owner.name or file.repository.owner.login,
        "updated_at": file.repository.updated_at.strftime("%Y-%m-%d"),
        "url": repo_url,
        "github_stars": file.repository.stargazers_count,
    }


def fetch_core_workers(github: Github) -> list[dict]:
    """Fetch workers from the openrelik-workers monorepo.

    Args:
        github: Authenticated PyGithub instance.

    Returns:
        List of worker item dicts.
    """
    items = []
    repo_name = "openrelik/openrelik-workers"
    base_path = "workers"

    try:
        repo = github.get_repo(repo_name)
        contents = repo.get_contents(base_path)
        for content_file in contents:
            if content_file.type == "dir":
                # Check for openrelik.yaml in this directory
                yaml_path = f"{content_file.path}/openrelik.yaml"
                try:
                    yaml_path = f"{content_file.path}/openrelik.yaml"
                    yaml_file = repo.get_contents(yaml_path)
                    log.debug("Processing monorepo worker: %s", yaml_path)
                    yaml_content = fetch_yaml_content(yaml_file.download_url)
                    if yaml_content:
                        item = build_item(yaml_file, yaml_content)
                        if item:
                            items.append(item)
                except GithubException:
                    log.debug("No openrelik.yaml in %s", content_file.path)
                    continue
    except GithubException as e:
        log.error("Failed to fetch monorepo %s: %s", repo_name, e)

    return items


def fetch_community_workers(github: Github) -> list[dict]:
    """Search GitHub for openrelik.yaml files and return worker items.

    Args:
        github: Authenticated PyGithub instance.

    Returns:
        List of worker item dicts.
    """
    # 1. Search by filename across GitHub
    query = "filename:openrelik.yaml -repo:openrelik/openrelik-workers"
    results = github.search_code(query=query)

    items = []
    processed_repos = set()

    for file in results:
        repo_full_name = file.repository.full_name
        log.debug("Found via code search: %s/%s", repo_full_name, file.path)

        yaml_content = fetch_yaml_content(file.download_url)
        if yaml_content is None:
            continue

        item = build_item(file, yaml_content)
        if item is not None:
            items.append(item)
            processed_repos.add(repo_full_name)

    # 2. Fallback: Search for repositories with 'openrelik-worker' in name
    # This helps when code search indexing is delayed or misses files.
    log.info("Running fallback repository search...")
    repo_query = "openrelik-worker in:name"
    repo_results = github.search_repositories(query=repo_query)

    for repo in repo_results:
        if repo.full_name in processed_repos or repo.owner.login.lower() == "openrelik":
            continue

        try:
            # Check for openrelik.yaml in the root
            yaml_file = repo.get_contents("openrelik.yaml")
            yaml_content = fetch_yaml_content(yaml_file.download_url)
            if yaml_content:
                item = build_item(yaml_file, yaml_content)
                if item:
                    items.append(item)
                    processed_repos.add(repo.full_name)
        except GithubException:
            # File not in root, skip for now as deeper search is expensive
            log.debug("No openrelik.yaml in root of %s", repo.full_name)
            continue

    return items


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search GitHub for openrelik.yaml and generate workerhub JSON data.",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN", ""),
        help="GitHub personal access token (default: $GITHUB_TOKEN)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("astro/src/data/workers.json"),
        help="Output file path (default: astro/src/data/workers.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print JSON to stdout instead of writing to file",
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

    github = Github(auth=Auth.Token(args.token))

    log.info("Fetching core workers...")
    items = fetch_core_workers(github)
    log.info("Found %d items in monorepo", len(items))

    log.info("Searching GitHub for community workers...")
    items.extend(fetch_community_workers(github))
    log.info("Found %d total published workers", len(items))

    # Sort items: OpenRelik-owned first, then by display_name
    items.sort(key=lambda x: (x["owner"] != "OpenRelik", x["display_name"].lower()))

    output_json = json.dumps({"workers": items}, indent=2, ensure_ascii=False)

    if args.dry_run:
        print(output_json)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_json)
        log.info("Wrote %s", args.output)

    log.info("Unpublished workers (skipped): %d", len(unpublished_workers))
    for repo in sorted(unpublished_workers):
        log.info("  %s", repo)

    return 0


if __name__ == "__main__":
    sys.exit(main())
