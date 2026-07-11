from __future__ import annotations

from authomatic.adapters import BaseAdapter
from pas.plugins.authomatic import logger
from typing import TYPE_CHECKING

import http.cookies


if TYPE_CHECKING:
    from pas.plugins.authomatic.browser.view import AuthomaticView


class ZopeRequestAdapter(BaseAdapter):
    """Adapter for Zope2 requests package."""

    def __init__(self, view: AuthomaticView) -> None:
        """
        :param view:
            BrowserView
        """
        self.view = view

    # =========================================================================
    # Request
    # =========================================================================

    @property
    def url(self) -> str:
        view_url = self.view.context.absolute_url()
        url = f"{view_url}/authomatic-handler/{self.view.provider}"
        logger.debug("url" + url)
        return url

    @property
    def params(self) -> dict:
        return dict(self.view.request.form)

    @property
    def cookies(self) -> dict[str, str]:
        # special handling since zope parsing does to much decoding
        cookie = http.cookies.SimpleCookie()
        cookie.load(self.view.request["HTTP_COOKIE"])
        cookies = {k: c.value for k, c in cookie.items()}
        return cookies

    # =========================================================================
    # Response
    # =========================================================================

    def write(self, value: str) -> None:
        logger.debug("write " + value)
        self.view.request.response.write(value)

    def set_header(self, key: str, value: str) -> None:
        logger.info("set_header " + key + "=" + value)
        self.view.request.response.setHeader(key, value)

    def set_status(self, status: str) -> None:
        raw_code, _ = status.split(" ")
        code = int(raw_code)
        logger.debug(f"set_status {code}")
        self.view.request.response.setStatus(code)
