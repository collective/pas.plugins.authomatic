# -*- coding: utf-8 -*-
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

_ = MessageFactory('pas.plugins.authomatic')


class IPasPluginsAuthomaticLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPasPluginsAuthomaticSettings(Interface):

    json_config = schema.SourceText(
        title=_(u"JSON Configuration"),
        required=True,
        default=u'',
    )


class IAuthomaticPlugin(Interface):
    """Member Properties To Group Plugin"""

