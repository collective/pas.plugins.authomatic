from pas.plugins.authomatic.testing import ACCEPTANCE_TESTING
from pas.plugins.authomatic.testing import FUNCTIONAL_TESTING
from pas.plugins.authomatic.testing import INTEGRATION_TESTING
from pas.plugins.authomatic.testing import RESTAPI_TESTING
from pytest_plone import fixtures_factory

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
        (ACCEPTANCE_TESTING, "acceptance"),
        (RESTAPI_TESTING, "restapi"),
    ))
)


@pytest.fixture
def plugin_id():
    return "authomatic"


@pytest.fixture
def add_plugin():
    def func(aclu, plugin_id):
        from pas.plugins.authomatic.setuphandlers import _add_plugin

        result = _add_plugin(aclu, plugin_id)
        return result

    return func


@pytest.fixture
def mock_result():
    class MockResult(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__dict__ = self

        def to_dict(self):
            return self

    return MockResult


@pytest.fixture
def mock_credentials(mock_result):
    class MockCredentials(mock_result):
        def refresh(*args):
            pass

    return MockCredentials


@pytest.fixture
def make_user(mock_result):
    mock = mock_result

    def make_user(login, plugin=None, password=None):
        from pas.plugins.authomatic.useridentities import UserIdentities

        uis = UserIdentities(login)
        if password:
            uis._secret = password
        plugin._useridentities_by_userid[login] = uis
        mock_result = mock(provider=mock(name="mock_provider"), user=mock())
        uis.handle_result(mock_result)
        return uis

    return make_user
