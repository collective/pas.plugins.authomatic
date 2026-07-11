from __future__ import annotations

from .base import BaseUserIDFactory
from pas.plugins.authomatic import _
from pas.plugins.authomatic import _types as t
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


class ProviderIDUserNameIdFactory(BaseUserIDFactory):
    title = _("Provider User Name or User ID")

    def __call__(self, plugin: AuthomaticPlugin, result: t.AuthResult) -> str:
        user_id = result.user.username or ""
        if not user_id:
            user_id = result.user.id or ""
        return self.normalize(plugin, result, user_id)
