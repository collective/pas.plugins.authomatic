# -*- coding: utf-8 -*-
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
import random
import string

_ = MessageFactory('pas.plugins.authomatic')

DEFAULT_ID = 'authomatic'

DEFAULT_CONFIG = u"""\
{
    "github": {
        display: {
            "title": "Github",
            "cssclasses": {
                "button": "btn btn-default",
                "icon": "glypicon glyphicon-github"
            },
            "as_form": false,
        },
        "class_": "authomatic.oauth2.GitHub",
        "consumer_key": "Example, please get a key and secret. See",
        "consumer_secret": "https://github.com/settings/applications/new",
        "access_headers": {
            "User-Agent": "Plone (pas.plugins.authomatic)"
        }
    }
}
"""

random_secret = u''.join(
    random.SystemRandom().choice(
        string.ascii_letters + string.digits
    ) for _ in range(10)
)


class IPasPluginsAuthomaticLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPasPluginsAuthomaticSettings(Interface):

    secret = schema.TextLine(
        title=_(u"Secret"),
        description=_(u"Some random string used to encrypt the state."),
        required=True,
        default=random_secret,
    )

    json_config = schema.SourceText(
        title=_(u"JSON Configuration"),
        description=_(
            u"Configuration parameters for the different authorization "
            u"providers. Details at "
            u"http://peterhudec.github.io/authomatic/reference/providers.html"
            u" - difference: 'class_' has to be a string, which is then "
            u"resolved as a dotted path."
        ),
        required=True,
        default=DEFAULT_CONFIG,
    )


class IAuthomaticPlugin(Interface):
    """Member Properties To Group Plugin"""
