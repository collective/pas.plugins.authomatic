from pas.plugins.authomatic.useridfactories import username

import pytest


class TestFactory:
    factory = username.ProviderIDUserNameFactory

    @pytest.fixture(autouse=True)
    def setup(self, user_data, plugin, auth_result_factory):
        self.result = auth_result_factory(user_data)
        self.user_id = self.result.user.username
        self.plugin = plugin

    def test_factory(self):
        """Test that the ProviderIDUserNameFactory generates a valid user ID."""
        factory_instance = self.factory()
        user_id = factory_instance(self.plugin, self.result)
        assert user_id == self.user_id

    def test_second_call_same_user_id(self):
        factory_instance = self.factory()
        # Simulate that the user ID is already taken
        self.plugin._useridentities_by_userid[self.user_id] = {"Some": "data"}
        user_id = factory_instance(self.plugin, self.result)
        assert user_id.startswith(self.user_id)
        assert (
            user_id == f"{self.user_id}_2"
        )  # The second call should append "_2" to the user ID
