from __future__ import annotations

from pas.plugins.authomatic._types import AuthResult
from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.interfaces import IUserIDFactory
from pas.plugins.authomatic.utils import authomatic_settings
from typing import TYPE_CHECKING
from zope.component import queryUtility
from zope.interface import implementer

import uuid


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


@implementer(IUserIDFactory)
class BaseUserIDFactory:
    def normalize(
        self, plugin: AuthomaticPlugin, result: AuthResult, userid: str
    ) -> str:
        new_userid = userid
        counter = 2  # first was taken, so logically its second
        while new_userid in plugin._useridentities_by_userid:
            new_userid = f"{userid}_{counter}"
            counter += 1
        return new_userid


class UUID4UserIDFactory(BaseUserIDFactory):
    title = _("UUID as User ID")

    def __call__(self, plugin: AuthomaticPlugin, result: AuthResult) -> str:
        return self.normalize(plugin, result, str(uuid.uuid4()))


class ProviderIDUserIDFactory(BaseUserIDFactory):
    title = _("Provider User ID")

    def __call__(self, plugin: AuthomaticPlugin, result: AuthResult) -> str:
        return self.normalize(plugin, result, result.user.id)


class ProviderIDUserNameFactory(BaseUserIDFactory):
    title = _("Provider User Name")

    def __call__(self, plugin: AuthomaticPlugin, result: AuthResult) -> str:
        return self.normalize(plugin, result, result.user.username)


def new_userid(plugin: AuthomaticPlugin, result: AuthResult) -> str:
    settings = authomatic_settings()
    factory = queryUtility(
        IUserIDFactory, name=settings.userid_factory_name, default=UUID4UserIDFactory()
    )
    return factory(plugin, result)


class ProviderIDUserNameIdFactory(BaseUserIDFactory):
    title = _("Provider User Name or User ID")

    def __call__(self, plugin: AuthomaticPlugin, result: AuthResult) -> str:
        user_id = result.user.username
        if not user_id:
            user_id = result.user.id
        return self.normalize(plugin, result, user_id)
