"""Application for testing and debugging http requests.

Allows setting up custom urls returning predefined responses.
"""

# importing lookups for registration
from http_stubs.lookups import *  # noqa: WPS347

default_app_config = 'http_stubs.apps.HttpStubsConfig'
