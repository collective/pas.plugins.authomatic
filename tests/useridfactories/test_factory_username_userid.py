from pas.plugins.authomatic.useridfactories import username_userid

import pytest


class TestFactory:
    factory = username_userid.ProviderIDUserNameIdFactory

    @pytest.fixture(autouse=True)
    def setup(self, user_data, plugin, auth_result_factory):
        self.result = auth_result_factory(user_data)
        self.plugin = plugin

    def test_factory_uses_username(self):
        """When a username is present, it is used as the user ID."""
        factory_instance = self.factory()
        user_id = factory_instance(self.plugin, self.result)
        assert user_id == self.result.user.username

    def test_factory_falls_back_to_user_id(self, auth_result_factory):
        """When the username is empty, the provider user id is used instead."""
        result = auth_result_factory({"id": "12345", "username": "", "email": ""})
        factory_instance = self.factory()
        user_id = factory_instance(self.plugin, result)
        assert user_id == result.user.id

    def test_second_call_same_user_id(self):
        factory_instance = self.factory()
        # Simulate that the user ID is already taken
        self.plugin._useridentities_by_userid[self.result.user.username] = {
            "Some": "data"
        }
        user_id = factory_instance(self.plugin, self.result)
        assert user_id == f"{self.result.user.username}_2"
