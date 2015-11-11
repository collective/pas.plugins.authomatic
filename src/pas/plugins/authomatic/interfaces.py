# -*- coding: utf-8 -*-
from zope import schema
from zope.component import getUtilitiesFor
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.interface import provider
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import random
import string

_ = MessageFactory('pas.plugins.authomatic')

DEFAULT_ID = 'authomatic'

DEFAULT_CONFIG = u"""\
{
    "github": {
        "display": {
            "title": "Github",
            "cssclasses": {
                "button": "plone-btn plone-btn-default",
                "icon": "glypicon glyphicon-github"
            },
            "as_form": false
        },
        "propertymap": {
            "email": "email",
            "link": "home_page",
            "location": "location",
            "name": "fullname"
        },
        "class_": "authomatic.providers.oauth2.GitHub",
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


@provider(IVocabularyFactory)
def userid_factory_vocabulary(context):
    items = []
    for name, factory in getUtilitiesFor(IUserIDFactory):
        items.append([factory.title, name])
    items = [SimpleTerm(name, name, title) for title, name in sorted(items)]
    return SimpleVocabulary(items)


class IPasPluginsAuthomaticSettings(Interface):

    secret = schema.TextLine(
        title=_(u"Secret"),
        description=_(u"Some random string used to encrypt the state."),
        required=True,
        default=random_secret,
    )
    userid_factory_name = schema.Choice(
        vocabulary="pas.plugins.authomatic.userid_vocabulary",
        title=u"Generator for Plone usernames to be used",
        description=u"",
        default='uuid'
    )
    json_config = schema.SourceText(
        title=_(u"JSON Configuration"),
        description=_(
            u"Configuration parameters for the different authorization "
            u"providers. Details at "
            u"http://peterhudec.github.io/authomatic/reference/providers.html"
            u" - difference: 'class_' has to be a string, which is then "
            u"resolved as a dotted path. Also sections ``display`` and "
            u"``propertymap`` are special"
        ),
        required=True,
        default=DEFAULT_CONFIG,
    )


class IAuthomaticPlugin(Interface):
    """Member Properties To Group Plugin"""

    def remember(result):
        """remember user as valid

        result is authomatic result data.
        """


class IUserIDFactory(Interface):
    """generates a userid on call
    """

    def __call__(service_name, service_user_id, raw_user):
        """returns string, unique amongst plugins userids
        """


class IPasPluginsAuthomaticLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
