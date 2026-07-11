from __future__ import annotations

from authomatic.adapters import BaseAdapter
from pas.plugins.authomatic import logger
from pas.plugins.authomatic import utils
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pas.plugins.authomatic.services.authomatic import LoginAuthomatic


Headers = dict | None


class RestAPIAdapter(BaseAdapter):
    """Adapter for plone.restapi usage."""

    headers: dict[str, str]
    frontend_route: str = "login-authomatic"

    def __init__(
        self,
        view: LoginAuthomatic,
        provider: str,
        params: Headers = None,
        cookies: Headers = None,
    ) -> None:
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
    def params(self) -> dict:
        """HTTP parameters (GET/POST).

        :returns: Dictionary with HTTP parameters.
        """
        return self._params or utils.extract_adapter_params(self.view.request)

    @property
    def cookies(self) -> dict:
        """Cookies information.

        :returns: Dictionary with cookies to be passed to Authomatic.
        """
        return self._cookies

    # =========================================================================
    # Response
    # =========================================================================

    def write(self, value: str) -> None:
        """Log Authomatic attempts to write to response."""
        logger.debug(f"Authomatic wrote {value} to response.")

    def set_header(self, key: str, value: str) -> None:
        """Store Authomatic header values.

        :params key: Header key.
        :params value: Header value.
        """
        self.headers[key] = value
        logger.debug(f"Authomatic set header {key} with {value}to response.")

    def set_status(self, status: int) -> None:
        """Log Authomatic attempts to set status code to response.

        :param status: Status code.
        """
        logger.debug(f"Authomatic set code {status} to response.")
