from pas.plugins.authomatic import utils

import pytest


class TestAuthomaticPlugin:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.portal = portal_class

    def test_authomatic_plugin_installed(self, plugin_id):
        from pas.plugins.authomatic.plugin import AuthomaticPlugin

        plugin = utils.authomatic_plugin()
        assert isinstance(plugin, AuthomaticPlugin)
        assert plugin.getId() == plugin_id
