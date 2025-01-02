from os import getenv

from dotenv import load_dotenv
from sharepoint_wrapper import SharePointConfig

load_dotenv()


class Config:
    # Sharepoint Configuration
    SHAREPOINT_CLIENT_ID = getenv("SHAREPOINT_CLIENT_ID")
    SHAREPOINT_CLIENT_SECRET = getenv("SHAREPOINT_CLIENT_SECRET")
    SHAREPOINT_TENANT = getenv("SHAREPOINT_TENANT")
    SHAREPOINT_TENANT_DOMAIN = getenv("SHAREPOINT_TENANT_DOMAIN")
    SHAREPOINT_SITE = getenv("SHAREPOINT_SITE")
    SHAREPOINT_PATH = getenv("SHAREPOINT_PATH")

    SHAREPOINT_CONFIG = SharePointConfig(
        tenant=SHAREPOINT_TENANT,
        tenant_domain=SHAREPOINT_TENANT_DOMAIN,
        client_id=SHAREPOINT_CLIENT_ID,
        client_secret=SHAREPOINT_CLIENT_SECRET,
        site=SHAREPOINT_SITE,
    )


config = Config()
