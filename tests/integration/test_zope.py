from pas.plugins.authomatic.integration.zope import ZopeRequestAdapter
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def view():
    view = MagicMock()
    view.context.absolute_url.return_value = "http://example.org/site"
    view.provider = "github"
    view.request.form = {"code": "abc", "state": "xyz"}
    view.request.__getitem__.return_value = "authomatic=cookievalue"
    return view


class TestZopeRequestAdapter:
    def test_url(self, view):
        adapter = ZopeRequestAdapter(view)
        assert adapter.url == "http://example.org/site/authomatic-handler/github"

    def test_params(self, view):
        adapter = ZopeRequestAdapter(view)
        assert adapter.params == {"code": "abc", "state": "xyz"}

    def test_cookies(self, view):
        # The raw HTTP_COOKIE header is parsed with SimpleCookie.
        adapter = ZopeRequestAdapter(view)
        assert adapter.cookies == {"authomatic": "cookievalue"}

    def test_write(self, view):
        adapter = ZopeRequestAdapter(view)
        adapter.write("payload")
        view.request.response.write.assert_called_once_with("payload")

    def test_set_header(self, view):
        adapter = ZopeRequestAdapter(view)
        adapter.set_header("Location", "http://example.org/next")
        view.request.response.setHeader.assert_called_once_with(
            "Location", "http://example.org/next"
        )

    def test_set_status(self, view):
        # Authomatic passes a status line like ``"302 Found"``.
        adapter = ZopeRequestAdapter(view)
        adapter.set_status("302 Found")
        view.request.response.setStatus.assert_called_once_with(302)
