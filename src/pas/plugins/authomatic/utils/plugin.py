from __future__ import annotations

from pas.plugins.authomatic.config import DEFAULT_ID
from plone import api
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


def authomatic_plugin() -> AuthomaticPlugin | None:
    """returns the authomatic pas-plugin instance"""
    aclu = api.portal.get_tool("acl_users")
    # XXX we should better iterate over all plugins and fetch the
    # authomatic plugin. There could be even 2 of them, even if this does not
    # make sense.
    return aclu.get(DEFAULT_ID, None)
