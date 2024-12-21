from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from plone import api
from plone.app.testing import logout

import json
import pytest


class TestControlPanel:
    @pytest.fixture(autouse=True)
    def _initialize(self, http_request, portal):
        self.portal = portal
        self.request = http_request

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def test_authomatic_controlpanel_view(self):
        view = api.content.get_view(
            name="authomatic-controlpanel", context=self.portal, request=self.request
        )
        assert view()

    def test_authomatic_controlpanel_view_protected(self):
        from AccessControl import Unauthorized

        logout()
        with pytest.raises(Unauthorized) as exc:
            self.portal.restrictedTraverse("@@authomatic-controlpanel")
        assert "Unauthorized('@@authomatic-controlpanel'" in str(exc)

    def test_authomatic_in_controlpanel(self):
        portal_controlpanel = api.portal.get_tool("portal_controlpanel")
        cp_ids = [a.getAction(self)["id"] for a in portal_controlpanel.listActions()]
        assert "authomatic" in cp_ids

    def test_json_config_property(self):
        assert "json_config" in IPasPluginsAuthomaticSettings
        value = api.portal.get_registry_record(
            name="json_config", interface=IPasPluginsAuthomaticSettings
        )
        assert isinstance(value, str)

    @pytest.mark.parametrize(
        "path,expected",
        [
            ["github/class_", "authomatic.providers.oauth2.GitHub"],
            ["github/consumer_key", "Example, please get a key and secret. See"],
            ["github/consumer_secret", "https://github.com/settings/applications/new"],
            ["github/id", 1],
            ["github/propertymap/email", "email"],
            ["github/propertymap/link", "home_page"],
            ["github/propertymap/location", "location"],
            ["github/propertymap/name", "fullname"],
        ],
    )
    def test_json_config_default(self, path, expected):
        value = json.loads(
            api.portal.get_registry_record(
                name="json_config", interface=IPasPluginsAuthomaticSettings
            )
        )
        for segment in path.split("/"):
            value = value[segment]
        assert value == expected
