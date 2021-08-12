from authomatic.adapters import BaseAdapter
from typing import Dict
from typing import Optional

import logging


logger = logging.getLogger(__file__)


Headers = Optional[Dict]


class RestAPIAdapter(BaseAdapter):
    """Adapter for plone.restapi usage."""

    frontend_route: str = "login-authomatic"

    def __init__(
        self, view, provider: str, params: Headers = None, cookies: Headers = None
    ):
        """Initialize the adapter.

        :param view: Service
        :param provider: ID of the Authomatic provider.
        :param params: Query string parameters, parsed as a dictionary.
        :param cookies: Dictionary with cookies information.
        """
        self.view = view
        self.public_url = view.public_url
        self.provider = provider
        self.headers = {}
        self._cookies = cookies if cookies else {}
        self._params = params

    # =========================================================================
    # Request
    # =========================================================================

    @property
    def url(self) -> str:
        """OAuth redirection URL.

        :returns: URL to be used in the redirection.
        """
        return f"{self.public_url}/{self.frontend_route}/{self.provider}"

    @property
    def params(self):
        """HTTP parameters (GET/POST).

        :returns: Dictionary with HTTP parameters.
        """
        params = self._params
        if not params:
            params = dict(self.view.request.form)
            to_remove = ["provider", "publicUrl"]
            params = {k: v for k, v in params.items() if k not in to_remove}
        return params

    @property
    def cookies(self) -> dict:
        """Cookies information.

        :returns: Dictionary with cookies to be passed to Authomatic.
        """
        return self._cookies

    # =========================================================================
    # Response
    # =========================================================================

    def write(self, value: str):
        """Log Authomatic attempts to write to response."""
        logger.debug(f"Authomatic wrote {value} to response.")

    def set_header(self, key: str, value: str):
        """Store Authomatic header values.

        :params key: Header key.
        :params value: Header value.
        """
        self.headers[key] = value
        logger.debug(f"Authomatic set header {key} with {value}to response.")

    def set_status(self, status: int):
        """Log Authomatic attempts to set status code to response.

        :param status: Status code.
        """
        logger.debug(f"Authomatic set code {status} to response.")
