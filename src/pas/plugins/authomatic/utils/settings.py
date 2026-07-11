from __future__ import annotations

from pas.plugins.authomatic import _types as t
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.dottedname.resolve import resolve

import json


def authomatic_settings() -> t.PasPluginsAuthomaticSettings:
    """fetches the authomatic settings from registry"""
    registry = queryUtility(IRegistry)
    return registry.forInterface(IPasPluginsAuthomaticSettings)


def authomatic_cfg() -> t.AuthomaticConfig:
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
    for name in cfg:
        provider = cfg[name]
        if "class_" in provider:
            provider["class_"] = resolve(provider["class_"])
        if "id" in provider:
            provider["id"] = int(provider["id"])
        else:
            # pick some id
            while cnt in ids:
                cnt += 1
            provider["id"] = cnt
        ids.update([provider["id"]])
    return cfg


def list_providers(base_url: str) -> list[t.LoginProvider]:
    """List all configured Authomatic plugins.

    :returns: List of login options.
    """
    providers = authomatic_cfg()
    plugins = []
    for provider_id, provider in providers.items():
        entry = provider.get("display", {})
        title = entry.get("title", provider_id)

        plugins.append({
            "id": provider_id,
            "plugin": "authomatic",
            "title": title,
            "url": f"{base_url}/@login-authomatic/{provider_id}",
        })
    return plugins
