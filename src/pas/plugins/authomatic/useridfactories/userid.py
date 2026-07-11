from .base import BaseUserIDFactory
from pas.plugins.authomatic import _
from pas.plugins.authomatic import _types as t
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


class ProviderIDUserIDFactory(BaseUserIDFactory):
    title = _("Provider User ID")

    def __call__(self, plugin: AuthomaticPlugin, result: t.AuthResult) -> str:
        user_id = result.user.id or ""
        return self.normalize(plugin, result, user_id)
