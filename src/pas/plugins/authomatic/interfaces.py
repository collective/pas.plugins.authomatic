# -*- coding: utf-8 -*-
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.interface import Invalid
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

_ = MessageFactory('pas.plugins.authomatic')


class IPasPluginsAuthomaticLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPasPluginsAuthomaticSettings(Interface):
    pass


class IAuthomaticPlugin(Interface):
    """Member Properties To Group Plugin"""
