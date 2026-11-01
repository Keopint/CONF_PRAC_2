from unittest.mock import patch
from src.fetcher import get_direct_dependencies


@patch("src.fetcher.fetch_package_metadata")
def test_get_direct_dependencies_success(mock_fetch):
    """Tests successful extraction of dependencies."""
    mock_fetch.return_value = {
        "info": {
            "requires_dist": ["requests>=2.0", "urllib3"]
        }
    }

    result = get_direct_dependencies("https://pypi.org", "test-pkg")
    assert result == ["requests", "urllib3"]


@patch("src.fetcher.fetch_package_metadata")
def test_get_direct_dependencies_empty(mock_fetch):
    """Tests extraction when no dependencies exist."""
    mock_fetch.return_value = {"info": {}}

    result = get_direct_dependencies("https://pypi.org", "empty-pkg")
    assert result == []