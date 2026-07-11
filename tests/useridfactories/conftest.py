from authomatic.core import User
from authomatic.providers import oauth2
from collections.abc import Callable
from dataclasses import dataclass
from pas.plugins.authomatic import _types as t
from pas.plugins.authomatic.plugin import AuthomaticPlugin
from typing import Any
from unittest.mock import MagicMock

import pytest


@dataclass
class LoginResult:
    user: User
    provider: t.AuthProvider
    error: Any = None


@pytest.fixture(scope="class")
def plugin() -> AuthomaticPlugin:

    plugin = AuthomaticPlugin(id="authomatic", title="Authomatic")
    return plugin


@pytest.fixture(scope="session")
def dummy_provider() -> oauth2.OAuth2:
    """An OAuth2 provider with mocked settings and adapter.

    The provider is only used to build :class:`~authomatic.core.User` and
    login-result instances, so the network-facing ``settings`` and ``adapter``
    collaborators are mocked away.
    """
    return oauth2.OAuth2(
        settings=MagicMock(),
        adapter=MagicMock(),
        provider_name="dummy",
    )


@pytest.fixture(scope="session")
def auth_user_factory(dummy_provider):

    def factory(user_data: dict[str, Any]) -> User:
        user = User(provider=dummy_provider, **user_data)
        return user

    return factory


@pytest.fixture(scope="session")
def auth_result_factory(
    dummy_provider, auth_user_factory
) -> Callable[[dict[str, Any]], t.AuthResult]:

    def factory(user_data: dict[str, Any]) -> LoginResult:
        user = auth_user_factory(user_data)
        provider = dummy_provider
        return LoginResult(user=user, provider=provider)

    return factory


@pytest.fixture(scope="class")
def user_data() -> dict[str, Any]:
    """Fixture providing sample user data for testing."""
    return {"id": "12345", "username": "testuser", "email": "foo@bar.com"}
