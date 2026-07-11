from pas.plugins.authomatic._types import AuthResult
from pas.plugins.authomatic.interfaces import IUserIDFactory
from typing import TYPE_CHECKING
from zope.interface import implementer


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
