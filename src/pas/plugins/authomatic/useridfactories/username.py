from __future__ import annotations

from .base import BaseUserIDFactory
from pas.plugins.authomatic import _
from pas.plugins.authomatic import _types as t
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


class ProviderIDUserNameFactory(BaseUserIDFactory):
    title = _("Provider User Name")

    def __call__(self, plugin: AuthomaticPlugin, result: t.AuthResult) -> str:
        username = result.user.username or ""
        return self.normalize(plugin, result, username)
