from pas.plugins.authomatic.integration.restapi import RestAPIAdapter
from unittest.mock import MagicMock
from zope.publisher.browser import TestRequest

import pytest


@pytest.fixture
def view():
    view = MagicMock()
    view.public_url = "http://example.org"
    view.request = TestRequest(form={"code": "abc", "provider": "github"})
    return view


class TestRestAPIAdapter:
    def test_url(self, view):
        adapter = RestAPIAdapter(view, "github")
        assert adapter.url == "http://example.org/login-authomatic/github"

    def test_params_from_explicit_value(self, view):
        adapter = RestAPIAdapter(view, "github", params={"a": "1"})
        assert adapter.params == {"a": "1"}

    def test_params_extracted_from_request(self, view):
        # ``provider`` is filtered out by ``extract_adapter_params``.
        adapter = RestAPIAdapter(view, "github")
        assert adapter.params == {"code": "abc"}

    def test_cookies_default_empty(self, view):
        adapter = RestAPIAdapter(view, "github")
        assert adapter.cookies == {}

    def test_cookies_from_explicit_value(self, view):
        adapter = RestAPIAdapter(view, "github", cookies={"authomatic": "xyz"})
        assert adapter.cookies == {"authomatic": "xyz"}

    def test_write_only_logs(self, view):
        # ``write`` must not touch the response, only log.
        adapter = RestAPIAdapter(view, "github")
        assert adapter.write("payload") is None

    def test_set_header_stores_value(self, view):
        adapter = RestAPIAdapter(view, "github")
        adapter.set_header("Location", "http://example.org/next")
        assert adapter.headers == {"Location": "http://example.org/next"}

    def test_set_status_is_noop(self, view):
        adapter = RestAPIAdapter(view, "github")
        assert adapter.set_status(302) is None
