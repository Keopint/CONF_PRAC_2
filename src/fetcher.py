import json
import re
import urllib.error
import urllib.request

HTTP_NOT_FOUND = 404


def clean_package_name(dependency_str: str) -> str:
    match = re.match(r"^[a-zA-Z0-9_\-\.]+", dependency_str)
    if match:
        return match.group(0)
    return dependency_str


def fetch_package_metadata(repo_url: str, package_name: str) -> dict:
    base_url = repo_url.rstrip("/")
    url = f"{base_url}/pypi/{package_name}/json"

    try:
        with urllib.request.urlopen(url) as response:
            raw_data = response.read().decode("utf-8")
            return json.loads(raw_data)
    except urllib.error.HTTPError as error:
        if error.code == HTTP_NOT_FOUND:
            raise ValueError(
                f"Package '{package_name}' not found in repository."
            ) from error
        raise ValueError(f"HTTP Error: {error.code}") from error
    except urllib.error.URLError as error:
        raise ValueError(
            f"Failed to reach repository: {error.reason}"
        ) from error
    except json.JSONDecodeError as error:
        raise ValueError(
            "Invalid JSON response from repository."
        ) from error


def get_direct_dependencies(repo_url: str, package_name: str) -> list[str]:
    metadata = fetch_package_metadata(repo_url, package_name)
    info = metadata.get("info", {})
    dependencies = info.get("requires_dist")

    if not dependencies:
        return []

    return [clean_package_name(dep) for dep in dependencies]