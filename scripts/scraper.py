# Copyright 2025 Google LLC
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

import requests
import yaml
from github import Auth, Github
import os


def search_github_for_openrelik_yaml(access_token: str) -> list:
    """
    Searches GitHub for files named 'openrelik.yaml'.

    Args:
        access_token: GitHub personal access token.

    Returns:
        A list of FileSearchResult objects or None if an error occurs.
    """
    auth = Auth.Token(access_token)
    github = Github(auth=auth)
    query = "filename:openrelik.yaml in:path language:yaml"
    results = github.search_code(query=query)
    return results


def display_results(results: list) -> str:
    """
    Displays the results of the GitHub search.

    Args:
        results: A list of FileSearchResult objects.

    Returns:
        A YAML formatted string containing the repository information.
    """
    repos = {"items": []}

    for file in results:
        if file.path != "openrelik.yaml":
            continue

        # Download the file content
        yaml_content = {}
        response = requests.get(file.download_url)
        if response.status_code == 200:
            file_content = response.text
            yaml_content = yaml.safe_load(file_content)
        else:
            print(f"Failed to download the file: {response.status_code}")
            continue

        # Worker metadata
        publish = yaml_content.get("publish", False)
        display_name = yaml_content.get("display_name", "N/A")
        description = yaml_content.get("description", "N/A")
        tools = yaml_content.get("tools", [])

        # Check if the repository should be published
        if not publish:
            continue

        if display_name.startswith("User-friendly"):
            display_name = file.repository.name

        if description.startswith("A brief description"):
            description = ""

        result = {
            "display_name": display_name,
            "description": description,
            "tools": tools,
            "repository": file.repository.full_name,
            "license": file.repository.license.name if file.repository.license else "N/A",
            "owner": file.repository.owner.name,
            "updated_at": file.repository.updated_at.strftime("%Y-%m-%d"),
            "url": file.repository.html_url,
            "github_stars": file.repository.stargazers_count,
        }
        repos["items"].append(result)

    return yaml.dump(repos, sort_keys=False)


if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    access_token = token if token else input("Enter your GitHub access token: ")
    results = search_github_for_openrelik_yaml(access_token)
    print(display_results(results))
