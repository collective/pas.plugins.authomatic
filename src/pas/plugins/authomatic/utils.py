from __future__ import annotations

from pas.plugins.authomatic._types import AuthomaticConfig
from pas.plugins.authomatic.interfaces import DEFAULT_ID
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from plone import api
from plone.registry.interfaces import IRegistry
from typing import TYPE_CHECKING
from zope.component import queryUtility
from zope.dottedname.resolve import resolve

import json


if TYPE_CHECKING:
    from pas.plugins.authomatic.plugin import AuthomaticPlugin


def authomatic_plugin() -> AuthomaticPlugin | None:
    """returns the authomatic pas-plugin instance"""
    aclu = api.portal.get_tool("acl_users")
    # XXX we should better iterate over all plugins and fetch the
    # authomatic plugin. There could be even 2 of them, even if this does not
    # make sense.
    return aclu.get(DEFAULT_ID, None)


def authomatic_settings() -> IPasPluginsAuthomaticSettings:
    """fetches the authomatic settings from registry"""
    registry = queryUtility(IRegistry)
    return registry.forInterface(IPasPluginsAuthomaticSettings)


def authomatic_cfg() -> AuthomaticConfig:
    """fetches the authomatic configuration from the settings and
    returns it as a dict

    Returns an empty dict when the configuration is missing or invalid, so
    callers can iterate over the result without a ``None`` check.
    """
    settings = authomatic_settings()
    try:
        cfg = json.loads(settings.json_config)
    except ValueError:
        return {}
    if not isinstance(cfg, dict):
        return {}
    ids = set()
    cnt = 1
    for provider in cfg:
        if "class_" in cfg[provider]:
            cfg[provider]["class_"] = resolve(cfg[provider]["class_"])
        if "id" in cfg[provider]:
            cfg[provider]["id"] = int(cfg[provider]["id"])
        else:
            # pick some id
            while cnt in ids:
                cnt += 1
            cfg[provider]["id"] = cnt
        ids.update([cfg[provider]["id"]])
    return cfg
