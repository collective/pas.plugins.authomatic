from pas.plugins.authomatic.useridfactories import new_userid
from uuid import UUID

import pytest


class TestNewUserID:
    """``new_userid`` dispatches to the factory named in the settings.

    This exercises the real registry + utility lookup, so it relies on the
    integration ``portal`` fixture (profile installed, factories registered).
    """

    @pytest.fixture(autouse=True)
    def setup(self, portal, plugin, auth_result_factory, user_data):
        self.portal = portal
        self.plugin = plugin
        self.result = auth_result_factory(user_data)

    def _set_factory_name(self, name: str):
        from plone import api

        api.portal.set_registry_record(
            "pas.plugins.authomatic.interfaces."
            "IPasPluginsAuthomaticSettings.userid_factory_name",
            name,
        )

    def test_dispatches_to_username_factory(self):
        self._set_factory_name("username")
        assert new_userid(self.plugin, self.result) == self.result.user.username

    def test_dispatches_to_userid_factory(self):
        self._set_factory_name("userid")
        assert new_userid(self.plugin, self.result) == self.result.user.id

    def test_dispatches_to_uuid_factory(self):
        self._set_factory_name("uuid")
        user_id = new_userid(self.plugin, self.result)
        assert str(UUID(user_id, version=4)) == user_id
