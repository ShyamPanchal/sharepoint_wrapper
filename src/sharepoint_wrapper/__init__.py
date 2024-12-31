from dataclasses import dataclass
from io import BytesIO

from sharepoint_wrapper._raw import (
    get_children,
    get_drives,
    get_file,
    get_graph_token,
    get_site,
    write_file,
)
from datetime import datetime, timedelta


@dataclass
class SharePointConfig:
    tenant: str
    tenant_domain: str
    client_id: str
    client_secret: str
    site: str

    _token: str = None
    _token_expiry = None
    _site_id: str = None
    _drive: str = None

    @property
    def token(self):
        now = datetime.now() - timedelta(minutes=5)
        if (
            self._token is not None
            and self._token_expiry is not None
            and now < self._token_expiry
        ):
            return self._token
        self._token, self._token_expiry = get_graph_token(
            self.tenant_domain, self.client_id, self.client_secret
        )
        return self._token

    @property
    def site_id(self):
        if self._site_id is not None:
            return self._site_id
        self._site_id = get_site(self.tenant, self.site, self.token)
        return self._site_id

    @property
    def drive(self):
        if self._drive is not None:
            return self._drive
        all_drives = get_drives(self.site_id, self.token)
        self._drive = all_drives[0][0]

        return self._drive


def get_folders(config: SharePointConfig, path: str | None = None):
    return get_children(config.drive, config.token, path, "folder")


def get_files(
    config: SharePointConfig,
    path: str | None = None,
    filter_params: dict | None = None,
    sort_params: list | None = None,
    detailed_response: bool | None = False,
):
    """
    Get files from SharePoint with advanced filtering options using Microsoft Graph API.

    Args:
        path: The folder path to get files from
        filter_params: Dictionary of OData filter expressions. Supported functions and operators:
            Comparison Operators:
                eq: Equal to
                ne: Not equal to
                gt: Greater than
                ge: Greater than or equal to
                lt: Less than
                le: Less than or equal to
            Logical Operators:
                and: Logical AND
                or: Logical OR
                not: Logical NOT
            String Functions:
                startswith(property, 'value'): Check if string starts with value
                endswith(property, 'value'): Check if string ends with value

            Supported Properties:
                name: File name
                webUrl: SharePoint URL

        sort_params: List of sort expressions. Format: ['property direction']
            Supported Properties:
                name: File name
                webUrl: SharePoint URL
                lastModifiedDateTime: last modified date time
            Directions:
                asc: Ascending order
                desc: Descending order

        detailed_response: Boolean flag to indicate if a detailed response is required. Defaults to False.

    Examples:
        # Filter by file name starting with "Report"
        client.get_files(
            path="/Documents",
            filter_params={
                "name": "startswith(name, 'Report')",
            }
        )

        # sort by modified date
        client.get_files(
            path="/Documents",
            sort_params=["lastModifiedDateTime desc"]
        )

    Returns:
        List of file items matching the specified criteria
    """
    return get_children(
        config.drive,
        config.token,
        path,
        "file",
        filter_params,
        sort_params,
        detailed_response,
    )


def get_file_content(config: SharePointConfig, file_name: str, path: str | None = None):
    return get_file(config.drive, config.token, file_name, path)


def upload_file(
    config: SharePointConfig,
    file_content: BytesIO,
    file_name: str,
    path: str | None = None,
):
    return write_file(config.drive, config.token, file_content, file_name, path)
