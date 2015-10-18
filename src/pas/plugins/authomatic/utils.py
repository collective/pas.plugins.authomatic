# -*- coding: utf-8 -*-
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.dottedname.resolve import resolve
import json


def authomatic_settings():
    registry = queryUtility(IRegistry)
    return registry.forInterface(
        IPasPluginsAuthomaticSettings
    )


def authomatic_cfg():
    settings = authomatic_settings()
    import pdb;pdb.set_trace();
    try:
        cfg = json.loads(settings.json_config)
    except ValueError:
        return None
    if not isinstance(cfg, dict):
        return None
    for provider in cfg:
        if 'class_' in cfg[provider]:
            cfg[provider]['class_'] = resolve(cfg[provider]['class_'])
    return cfg
