from __future__ import annotations

from .userid import ProviderIDUserIDFactory
from .username import ProviderIDUserNameFactory
from .username_userid import ProviderIDUserNameIdFactory
from .uuid_ import UUID4UserIDFactory
from pas.plugins.authomatic._types import AuthResult
from pas.plugins.authomatic.interfaces import IUserIDFactory
from pas.plugins.authomatic.utils import authomatic_settings
from typing import TYPE_CHECKING
from zope.component import queryUtility


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


def new_userid(plugin: AuthomaticPlugin, result: AuthResult) -> str:
    settings = authomatic_settings()
    factory = queryUtility(
        IUserIDFactory, name=settings.userid_factory_name, default=UUID4UserIDFactory()
    )
    return factory(plugin, result)


__all__ = (
    "ProviderIDUserIDFactory",
    "ProviderIDUserNameFactory",
    "ProviderIDUserNameIdFactory",
    "UUID4UserIDFactory",
    "new_userid",
)
