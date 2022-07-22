from authomatic.adapters import BaseAdapter

import http
import logging


logger = logging.getLogger(__file__)


class ZopeRequestAdapter(BaseAdapter):
    """Adapter for Zope2 requests package."""

    def __init__(self, view):
        """
        :param view:
            BrowserView
        """
        self.view = view

    # =========================================================================
    # Request
    # =========================================================================

    @property
    def url(self):
        view_url = self.view.context.absolute_url()
        url = f"{view_url}/authomatic-handler/{self.view.provider}"
        logger.debug("url" + url)
        return url

    @property
    def params(self):
        return dict(self.view.request.form)

    @property
    def cookies(self):
        # special handling since zope parsing does to much decoding
        cookie = http.cookies.SimpleCookie()
        cookie.load(self.view.request["HTTP_COOKIE"])
        cookies = {k: c.value for k, c in cookie.items()}
        return cookies

    # =========================================================================
    # Response
    # =========================================================================

    def write(self, value):
        logger.debug("write " + value)
        self.view.request.response.write(value)

    def set_header(self, key, value):
        logger.info("set_header " + key + "=" + value)
        self.view.request.response.setHeader(key, value)

    def set_status(self, status):
        code, message = status.split(" ")
        code = int(code)
        logger.debug(f"set_status {code}")
        self.view.request.response.setStatus(code)
