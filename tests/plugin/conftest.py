import pytest


@pytest.fixture
def plugin(portal, add_plugin, plugin_id):
    add_plugin(portal.acl_users, plugin_id)
    return portal.acl_users[plugin_id]
