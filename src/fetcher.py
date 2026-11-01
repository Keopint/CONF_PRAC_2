import json
import urllib.error
import urllib.request

HTTP_NOT_FOUND = 404


def fetch_package_metadata(repo_url: str, package_name: str) -> dict:
    """
    Fetches package metadata from PyPI JSON API.
    """
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

    # 'requires_dist' contains the list of dependencies
    dependencies = info.get("requires_dist")

    if not dependencies:
        return []

    return dependencies