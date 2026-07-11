from pas.plugins.authomatic.useridfactories import uuid_
from uuid import UUID

import pytest


class TestFactory:
    factory = uuid_.UUID4UserIDFactory

    @pytest.fixture(autouse=True)
    def setup(self, user_data, plugin, auth_result_factory):
        self.result = auth_result_factory(user_data)
        self.plugin = plugin

    def test_factory(self):
        """Test that the UUID4UserIDFactory generates a valid UUID4 user ID."""
        factory_instance = self.factory()
        user_id = factory_instance(self.plugin, self.result)

        # Check that the generated user ID is a valid UUID4
        try:
            uuid_obj = UUID(user_id, version=4)
        except ValueError:
            pytest.fail(f"Generated user ID '{user_id}' is not a valid UUID4.")

        assert str(uuid_obj) == user_id, (
            "The generated user ID does not match the expected UUID4 format."
        )
