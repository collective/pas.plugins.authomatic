from pas.plugins.authomatic import utils
from pas.plugins.authomatic.utils.settings import list_providers

import pytest


def set_json_config(value: str) -> None:
    from plone import api

    api.portal.set_registry_record(
        "pas.plugins.authomatic.interfaces.IPasPluginsAuthomaticSettings.json_config",
        value,
    )


class TestSettings:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.portal = portal_class

    def test_authomatic_settings(self):
        settings = utils.authomatic_settings()
        assert settings.json_config

    def test_authomatic_cfg_returns_default_provider(self):
        cfg = utils.authomatic_cfg()
        assert "github" in cfg
        # ``class_`` is resolved from its dotted path to the provider class.
        assert not isinstance(cfg["github"]["class_"], str)
        # ``id`` is coerced to an int.
        assert cfg["github"]["id"] == 1

    def test_authomatic_cfg_invalid_returns_empty_dict(self):
        set_json_config("{not valid json")
        assert utils.authomatic_cfg() == {}

    def test_authomatic_cfg_non_mapping_returns_empty_dict(self):
        set_json_config("[1, 2, 3]")
        assert utils.authomatic_cfg() == {}

    def test_authomatic_cfg_assigns_id_when_missing(self):
        set_json_config('{"provider_a": {}, "provider_b": {}}')
        cfg = utils.authomatic_cfg()
        # An id is auto-assigned to every provider lacking one, uniquely.
        assert cfg["provider_a"]["id"] == 1
        assert cfg["provider_b"]["id"] == 2


class TestListProviders:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.portal = portal_class

    def test_default_provider(self):
        providers = list_providers("http://example.org")
        assert providers == [
            {
                "id": "github",
                "plugin": "authomatic",
                "title": "Github",
                "url": "http://example.org/@login-authomatic/github",
            }
        ]

    def test_title_falls_back_to_provider_id(self):
        set_json_config('{"acme": {}}')
        providers = list_providers("http://example.org")
        assert providers == [
            {
                "id": "acme",
                "plugin": "authomatic",
                "title": "acme",
                "url": "http://example.org/@login-authomatic/acme",
            }
        ]

    def test_empty_when_not_configured(self):
        set_json_config("{not valid json")
        assert list_providers("http://example.org") == []
