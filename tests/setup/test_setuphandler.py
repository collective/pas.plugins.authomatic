import pytest


@pytest.fixture
def plugin(add_plugin, app, plugin_id):
    add_plugin(app.acl_users, plugin_id)
    return app.acl_users[plugin_id]


class TestSetupHandlers:
    @pytest.fixture(autouse=True)
    def _setup(self, app):
        self.aclu = app.acl_users

    def test_addplugin(self, add_plugin, plugin_id):
        from pas.plugins.authomatic.plugin import AuthomaticPlugin

        add_plugin(self.aclu, plugin_id)
        plugin = self.aclu[plugin_id]
        assert plugin_id in self.aclu.objectIds()

        assert isinstance(plugin, AuthomaticPlugin)

    def test_cannot_add_duplicated_plugin(self, plugin, add_plugin, plugin_id):
        from pas.plugins.authomatic.setuphandlers import TITLE

        assert plugin_id in self.aclu.objectIds()
        result = add_plugin(self.aclu, plugin_id)
        assert result == f"{TITLE} already installed."

    def test_removeplugin(self, plugin, plugin_id):
        from pas.plugins.authomatic.setuphandlers import _remove_plugin

        assert plugin_id in self.aclu.objectIds()
        _remove_plugin(self.aclu, pluginid=plugin_id)
        assert plugin_id not in self.aclu.objectIds()
