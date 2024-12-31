from unittest.mock import patch, MagicMock

import pytest
from sharepoint_wrapper import get_files

from tests.env import config


@pytest.fixture
def mock_config():
    return config.SHAREPOINT_CONFIG


@patch("sharepoint_wrapper._raw.http.request")
def test_get_files_with_detailed_response(mock_request, mock_config):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.data = b"""{"value": [{
            "createdBy": {
                "user": {
                    "displayName": "Jane Doe",
                    "email": "john.doe@example.com"
                }
            },
            "createdDateTime": "2024-12-19T10:27:01Z",
            "lastModifiedBy": {
                "user": {
                    "displayName": "Jane Doe",
                    "email": "jane.doe@example.com"
                }
            },
            "lastModifiedDateTime": "2024-12-30T11:56:09Z",
            "name": "example_file.xlsb",
            "file": {},
            "webUrl": "https://example.com/file"
        }]}"""
    mock_request.return_value = mock_response

    # Make the actual call
    result = get_files(
        config=mock_config,  # Use the fixture
        path=config.SHAREPOINT_PATH,
        filter_params={"name": "startswith(name,'Budgets')"},
        detailed_response=True,
    )

    # Verify the results
    assert len(result) == 1
    file_info = result[0]

    # Verify required fields exist and have correct data types
    assert isinstance(file_info["name"], str)
    assert isinstance(file_info["webUrl"], str)
    assert file_info["type"] == "file"

    # Verify nested structure exists without checking specific values
    assert "createdBy" in file_info
    assert "email" in file_info["createdBy"]
    assert isinstance(file_info["createdBy"]["email"], str)

    assert "lastModifiedBy" in file_info
    assert "email" in file_info["lastModifiedBy"]
    assert isinstance(file_info["lastModifiedBy"]["email"], str)

    # Verify datetime fields exist and have correct format
    assert "createdDateTime" in file_info
    assert "lastModifiedDateTime" in file_info

    # Verify request was made with proper authentication
    assert mock_request.called
    call_args = mock_request.call_args
    assert "Authorization" in call_args[1]["headers"]


@patch("sharepoint_wrapper._raw.http.request")
def test_get_files_without_detailed_response(mock_request, mock_config):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.data = b"""{"value": [{
               "name": "example_file.xlsb",
               "file": {},
               "webUrl": "https://example.com/file"
           }]}"""
    mock_request.return_value = mock_response

    result = get_files(
        config=mock_config,
        path=config.SHAREPOINT_PATH,
        filter_params={"name": "startswith(name,'Budgets')"},
        detailed_response=False,
    )

    assert len(result) == 1
    file_info = result[0]

    # Verify required fields exist and have correct data types
    assert isinstance(file_info["name"], str)
    assert isinstance(file_info["webUrl"], str)
    assert file_info["type"] == "file"

    assert mock_request.called
    call_args = mock_request.call_args
    assert "Authorization" in call_args[1]["headers"]


@patch("sharepoint_wrapper._raw.http.request")
def test_get_files_with_sorting(mock_request, mock_config):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.data = b"""{
            "value": [
                {
                    "name": "example_file1.xlsb",
                    "file": {},
                    "webUrl": "https://example1.com/file"
                },
                {
                    "name": "example_file2.xlsb",
                    "file": {},
                    "webUrl": "https://example2.com/file"
                 },
                {
                    "name": "example_file3.xlsb",
                    "file": {},
                    "webUrl": "https://example3.com/file"
                },
                {
                    "name": "example_file4.xlsb",
                    "file": {},
                    "webUrl": "https://example4.com/file"
                },
                {
                    "name": "example_file5.xlsb",
                    "file": {},
                    "webUrl": "https://example5.com/file"
                }
            ]
        }"""
    mock_request.return_value = mock_response

    result = get_files(
        config=mock_config, path=config.SHAREPOINT_PATH, sort_params=["name asc"]
    )

    assert len(result) == 5
    file_info = result[0]

    # Verify required fields exist and have correct data types
    assert isinstance(file_info["name"], str)
    assert isinstance(file_info["webUrl"], str)
    assert file_info["type"] == "file"

    assert mock_request.called
    call_args = mock_request.call_args
    assert "Authorization" in call_args[1]["headers"]


@patch("sharepoint_wrapper._raw.http.request")
def test_get_files_with_combined_filters(mock_request, mock_config):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.data = b"""{
                "value": [
                     {
                        "name": "example_file1.xlsb",
                        "file": {},
                        "webUrl": "https://example1.com/file"
                    },
                    {
                        "name": "example_file2.xlsb",
                        "file": {},
                        "webUrl": "https://example2.com/file"
                     },
                    {
                        "name": "example_file3.xlsb",
                        "file": {},
                        "webUrl": "https://example3.com/file"
                    }
                ]
            }"""
    mock_request.return_value = mock_response

    result = get_files(
        config=mock_config,
        path=config.SHAREPOINT_PATH,
        filter_params={"name": "startswith(name,'DGR')"},
        sort_params=["lastModifiedDateTime desc"],
    )

    assert len(result) == 3
    file_info = result[0]

    # Verify required fields exist and have correct data types
    assert isinstance(file_info["name"], str)
    assert isinstance(file_info["webUrl"], str)
    assert file_info["type"] == "file"

    assert mock_request.called
    call_args = mock_request.call_args
    assert "Authorization" in call_args[1]["headers"]
