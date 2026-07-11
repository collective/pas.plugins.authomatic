from pas.plugins.authomatic.browser import view as view_module
from pas.plugins.authomatic.browser.view import AuthomaticView
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME
from unittest.mock import MagicMock

import pytest


def set_json_config(value: str) -> None:
    api.portal.set_registry_record(
        "pas.plugins.authomatic.interfaces.IPasPluginsAuthomaticSettings.json_config",
        value,
    )


class TestAuthomaticView:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal
        self.request = portal.REQUEST
        self.view = AuthomaticView(portal, self.request)

    def _mock_authomatic(self, monkeypatch, result):
        auth = MagicMock()
        auth.login.return_value = result
        monkeypatch.setattr(view_module, "Authomatic", lambda *a, **kw: auth)

    # -- properties / helpers ------------------------------------------------

    def test_config_is_cached(self):
        assert "github" in self.view.config
        # second access returns the cached value
        assert self.view.config is self.view._config

    def test_provider_names(self):
        assert self.view._provider_names == ["github"]

    def test_provider_names_raises_when_unconfigured(self):
        set_json_config("{not valid json")
        view = AuthomaticView(self.portal, self.request)
        with pytest.raises(ValueError):
            _ = view._provider_names

    def test_providers(self):
        providers = list(self.view.providers())
        assert len(providers) == 1
        assert providers[0]["identifier"] == "github"
        assert providers[0]["title"] == "Github"
        assert providers[0]["as_form"] is False

    def test_providers_raises_when_unconfigured(self):
        set_json_config("{not valid json")
        view = AuthomaticView(self.portal, self.request)
        with pytest.raises(ValueError):
            list(view.providers())

    def test_publish_traverse_sets_provider(self):
        result = self.view.publishTraverse(self.request, "github")
        assert result is self.view
        assert self.view.provider == "github"

    def test_publish_traverse_keeps_first_provider(self):
        self.view.publishTraverse(self.request, "github")
        # A second traversal segment must not override the provider.
        self.view.publishTraverse(self.request, "extra")
        assert self.view.provider == "github"

    def test_aclu(self):
        assert self.view.aclu.getId() == "acl_users"

    def test_zope_request_adapter(self):
        from pas.plugins.authomatic.integration import ZopeRequestAdapter

        assert isinstance(self.view.zope_request_adapter, ZopeRequestAdapter)

    def test_is_anon(self):
        login(self.portal, TEST_USER_NAME)
        assert self.view.is_anon is False
        logout()
        assert self.view.is_anon is True

    def test_handle_error_with_message(self):
        error = MagicMock()
        error.message = "boom"
        assert self.view._handle_error(error) == "boom"

    def test_handle_error_without_message(self):
        assert self.view._handle_error("plain error") == "plain error"

    def test_redirect(self):
        assert self.view._redirect() == "redirecting"

    def test_add_identity_delegates_to_plugin(self, monkeypatch):
        aclu = MagicMock()
        monkeypatch.setattr(AuthomaticView, "aclu", property(lambda self: aclu))
        result = MagicMock()
        self.view._add_identity(result, "GitHub")
        aclu.authomatic.remember_identity.assert_called_once_with(result)

    def test_remember_identity_delegates_to_plugin(self, monkeypatch):
        aclu = MagicMock()
        monkeypatch.setattr(AuthomaticView, "aclu", property(lambda self: aclu))
        result = MagicMock()
        self.view._remember_identity(result, "GitHub")
        aclu.authomatic.remember.assert_called_once_with(result)

    # -- __call__ branches ---------------------------------------------------

    def test_call_not_configured(self):
        set_json_config("{not valid json")
        assert self.view() == "Authomatic is not configured"

    def test_call_redirects_when_not_root(self):
        with api.env.adopt_roles(["Manager"]):
            folder = api.content.create(
                container=self.portal, type="Folder", id="f1", title="F1"
            )
        view = AuthomaticView(folder, self.request)
        view.provider = "github"
        assert view() == "redirecting"

    def test_call_renders_template_without_provider(self, monkeypatch):
        monkeypatch.setattr(
            AuthomaticView, "template", lambda self: "TEMPLATE", raising=False
        )
        assert self.view() == "TEMPLATE"

    def test_call_provider_not_supported(self):
        self.view.provider = "unknown"
        assert self.view() == "Provider not supported"

    def test_call_authenticated_and_connected_redirects(self):
        # A logged-in user visiting an already-configured provider is
        # redirected before the OAuth flow starts.
        login(self.portal, TEST_USER_NAME)
        self.view.provider = "github"
        assert self.view() == "redirecting"

    def test_call_login_returns_none_when_no_result(self, monkeypatch):
        logout()
        self.view.provider = "github"
        self._mock_authomatic(monkeypatch, None)
        assert self.view() is None

    def test_call_login_handles_error(self, monkeypatch):
        logout()
        self.view.provider = "github"
        result = MagicMock()
        result.error.message = "oauth failed"
        self._mock_authomatic(monkeypatch, result)
        assert self.view() == "oauth failed"

    def test_call_login_success_anonymous_remembers_identity(self, monkeypatch):
        logout()
        self.view.provider = "github"
        result = MagicMock()
        result.error = None
        self._mock_authomatic(monkeypatch, result)
        calls = {}
        monkeypatch.setattr(
            AuthomaticView,
            "_remember_identity",
            lambda self, r, p: calls.setdefault("remember", (r, p)),
        )
        monkeypatch.setattr(AuthomaticView, "_redirect", lambda self: "redirected")
        assert self.view() == "redirected"
        assert calls["remember"][0] is result
