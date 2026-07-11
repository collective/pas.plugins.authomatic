from .base import BaseUserIDFactory
from pas.plugins.authomatic import _
from pas.plugins.authomatic import _types as t
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin

import uuid


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


class UUID4UserIDFactory(BaseUserIDFactory):
    title = _("UUID as User ID")

    def __call__(self, plugin: AuthomaticPlugin, result: t.AuthResult) -> str:
        return self.normalize(plugin, result, str(uuid.uuid4()))
