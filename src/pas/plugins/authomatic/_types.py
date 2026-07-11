"""Shared typing helpers for :mod:`pas.plugins.authomatic`.

This module centralizes the :class:`~typing.TypedDict` definitions used to
document the various mappings handled by the package -- provider
configuration, REST API replies and user enumeration results.
"""

from typing import Any
from typing import Protocol
from typing import TypedDict


class AuthProvider(Protocol):
    """Structural type for an ``authomatic`` provider instance.

    ``authomatic`` ships without type information, so we describe here only
    the surface consumed by this package.
    """

    name: str


class AuthUser(Protocol):
    """Structural type for :class:`authomatic.core.User`.

    Only the attributes and methods used by this package are declared. Fields
    are optional because ``authomatic`` populates them from provider data.
    """

    id: str | None
    username: str | None
    name: str | None
    email: str | None
    data: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]: ...

    def update(self) -> None: ...


class AuthResult(Protocol):
    """Structural type for :class:`authomatic.core.LoginResult`."""

    user: AuthUser
    provider: AuthProvider
    error: Any


class ProviderConfig(TypedDict, total=False):
    """Configuration for a single Authomatic provider.

    The values come from the user-provided JSON configuration, so every key
    is optional. ``class_`` is stored as a dotted-path string in the JSON but
    resolved to the provider class by :func:`.utils.authomatic_cfg`.
    """

    id: int
    class_: Any
    display: dict[str, Any]
    propertymap: dict[str, str | dict[str, str]]
    consumer_key: str
    consumer_secret: str
    access_headers: dict[str, str]


#: Mapping of provider name to its :class:`ProviderConfig`.
AuthomaticConfig = dict[str, ProviderConfig]


class ErrorDetail(TypedDict):
    """Body of an error returned by the REST API services."""

    type: str
    message: str


class ErrorReply(TypedDict):
    """Error reply envelope returned by the REST API services."""

    error: ErrorDetail


class NextURLReply(TypedDict):
    """Successful reply of the ``@login-authomatic`` GET service."""

    next_url: str
    session: str


class TokenReply(TypedDict):
    """Successful reply of the ``@login-authomatic`` POST service."""

    token: str


class UserInfo(TypedDict):
    """User enumeration entry returned by the PAS plugin."""

    id: str
    login: str
    pluginid: str


class LoginCredentials(TypedDict, total=False):
    """Credentials mapping passed to the PAS authentication plugin."""

    login: str
    password: str


class LoginProvider(TypedDict):
    """A possible login provider."""

    id: str
    plugin: str
    title: str
    url: str


class ProviderButton(TypedDict):
    """A provider entry rendered as a login button by the Classic UI view."""

    identifier: str
    title: str
    iconclasses: str
    buttonclasses: str
    as_form: bool
