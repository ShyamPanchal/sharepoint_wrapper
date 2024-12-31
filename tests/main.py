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
    mock_response.data = b'''{"value": [{
            "createdBy": {
                "user": {
                    "displayName": "Shah Kajal Jay",
                    "email": "shah.kajal@truboardpartners.com"
                }
            },
            "createdDateTime": "2024-12-19T10:27:01Z",
            "lastModifiedBy": {
                "user": {
                    "displayName": "Tumu Hasitha",
                    "email": "hasitha.tumu@truboardpartners.com"
                }
            },
            "lastModifiedDateTime": "2024-12-30T11:56:09Z",
            "name": "DGR_Serentica Bikaner_Rajasthan.xlsb",
            "file": {},
            "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BECE3630A-4199-4CC9-8CF3-A9DB1E0EBBEF%7D&file=DGR_Serentica%20Bikaner_Rajasthan.xlsb&action=default&mobileredirect=true"
        }]}'''
    mock_request.return_value = mock_response

    # Make the actual call
    result = get_files(
        config=mock_config,  # Use the fixture
        path="/DGR Report - Serentica",
        filter_params={"name": "startswith(name,'DGR_Serentica')"},
        detailed_response=True,
    )

    # Verify the results
    assert len(result) == 1
    assert result[0]["name"] == "DGR_Serentica Bikaner_Rajasthan.xlsb"
    assert result[0][
               "webUrl"] == "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BECE3630A-4199-4CC9-8CF3-A9DB1E0EBBEF%7D&file=DGR_Serentica%20Bikaner_Rajasthan.xlsb&action=default&mobileredirect=true"
    assert result[0]["type"] == "file"
    assert result[0]["createdBy"]["email"] == "shah.kajal@truboardpartners.com"
    assert result[0]["lastModifiedBy"]["email"] == "hasitha.tumu@truboardpartners.com"

    assert mock_request.called
    call_args = mock_request.call_args
    assert "Authorization" in call_args[1]["headers"]

@patch("sharepoint_wrapper._raw.http.request")
def test_get_files_without_detailed_response(mock_request, mock_config):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.data = b'''{"value": [{
               "name": "DGR_Serentica Bikaner_Rajasthan.xlsb",
               "file": {},
               "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BECE3630A-4199-4CC9-8CF3-A9DB1E0EBBEF%7D&file=DGR_Serentica%20Bikaner_Rajasthan.xlsb&action=default&mobileredirect=true"
           }]}'''
    mock_request.return_value = mock_response

    result = get_files(
        config=mock_config,
        path="/DGR Report - Serentica",
        filter_params={"name": "startswith(name,'DGR_Serentica')"},
        detailed_response=False
    )

    assert len(result) == 1
    assert result[0]["name"] == "DGR_Serentica Bikaner_Rajasthan.xlsb"
    assert result[0][
               "webUrl"] == "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BECE3630A-4199-4CC9-8CF3-A9DB1E0EBBEF%7D&file=DGR_Serentica%20Bikaner_Rajasthan.xlsb&action=default&mobileredirect=true"
    assert result[0]["type"] == "file"

    assert mock_request.called
    call_args = mock_request.call_args
    assert "Authorization" in call_args[1]["headers"]


@patch("sharepoint_wrapper._raw.http.request")
def test_get_files_with_sorting(mock_request, mock_config):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.data = b'''{
            "value": [
                {
                    "name": "Budgets_PVsyst.xlsx",
                    "file": {},
                    "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7B97BE3F07-3A40-4870-99E2-86BDF1EE6F7B%7D&file=Budgets_PVsyst.xlsx&action=default&mobileredirect=true"
                },
                {
                    "name": "DGR_Serentica Bikaner_Rajasthan.xlsb",
                    "file": {},
                    "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BECE3630A-4199-4CC9-8CF3-A9DB1E0EBBEF%7D&file=DGR_Serentica%20Bikaner_Rajasthan.xlsb&action=default&mobileredirect=true"
                 },
                {
                    "name": "DGR_SRI1PL_198MW Koppal 18-12-2024.xlsx",
                    "file": {},
                    "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BD37677BD-5A97-4F74-8B60-D73BFC7072BD%7D&file=DGR_SRI1PL_198MW%20Koppal%2018-12-2024.xlsx&action=default&mobileredirect=true"
                },
                {
                    "name": "DGR_SRI1PL_198MW Koppal 29-12-2024.xlsx",
                    "file": {},
                    "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7B9FD0B814-D922-4702-B8C3-85E84D0EC282%7D&file=DGR_SRI1PL_198MW%20Koppal%2029-12-2024.xlsx&action=default&mobileredirect=true"
                },
                {
                    "name": "Soiling Loss Sheet.xlsx",
                    "file": {},
                    "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7B8946C222-8DF7-454A-A4DC-F35F48880033%7D&file=Soiling%20Loss%20Sheet.xlsx&action=default&mobileredirect=true"
                }
            ]
        }'''
    mock_request.return_value = mock_response

    result = get_files(
        config=mock_config,
        path="/DGR Report - Serentica",
        sort_params=["name asc"]
    )

    assert len(result) == 5
    assert result[0]["name"] == "Budgets_PVsyst.xlsx"


@patch("sharepoint_wrapper._raw.http.request")
def test_get_files_with_combined_filters(mock_request, mock_config):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.data = b'''{
                "value": [
                     {
                        "name": "DGR_SRI1PL_198MW Koppal 18-12-2024.xlsx",
                        "file": {},
                        "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BD37677BD-5A97-4F74-8B60-D73BFC7072BD%7D&file=DGR_SRI1PL_198MW%20Koppal%2018-12-2024.xlsx&action=default&mobileredirect=true"
                    },
                    {
                        "name": "DGR_Serentica Bikaner_Rajasthan.xlsb",
                        "file": {},
                        "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7BECE3630A-4199-4CC9-8CF3-A9DB1E0EBBEF%7D&file=DGR_Serentica%20Bikaner_Rajasthan.xlsb&action=default&mobileredirect=true"
                     },
                    {
                        "name": "DGR_SRI1PL_198MW Koppal 29-12-2024.xlsx",
                        "file": {},
                        "webUrl": "https://truboardpartners.sharepoint.com/sites/ramstechdata/_layouts/15/Doc.aspx?sourcedoc=%7B9FD0B814-D922-4702-B8C3-85E84D0EC282%7D&file=DGR_SRI1PL_198MW%20Koppal%2029-12-2024.xlsx&action=default&mobileredirect=true"
                    }
                ]
            }'''
    mock_request.return_value = mock_response

    result = get_files(
        config=mock_config,
        path="/DGR Report - Serentica",
        filter_params={"name": "startswith(name,'DGR')"},
        sort_params=["lastModifiedDateTime desc"],
    )

    assert len(result) == 3
    assert result[0]["name"] == "DGR_SRI1PL_198MW Koppal 18-12-2024.xlsx"
