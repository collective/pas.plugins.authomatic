import pytest


@pytest.fixture
def plugin():
    from BTrees.OOBTree import OOBTree

    class MockPlugin:
        _useridentities_by_userid = OOBTree()

    return MockPlugin


class TestUserIDFactories:
    def test_normalizer(self, plugin, mock_result):
        from pas.plugins.authomatic.useridfactories import BaseUserIDFactory

        bf = BaseUserIDFactory()

        mock_plugin = plugin
        mock_result = mock_result()
        assert bf.normalize(mock_plugin, mock_result, "fo") == "fo"
        mock_plugin._useridentities_by_userid["fo"] = 1
        assert bf.normalize(mock_plugin, mock_result, "fo") == "fo_2"
