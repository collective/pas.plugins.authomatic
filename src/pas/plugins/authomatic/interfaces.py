from zope import schema
from zope.component import getUtilitiesFor
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import provider
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import json
import random
import string


_ = MessageFactory("pas.plugins.authomatic")

DEFAULT_ID = "authomatic"

DEFAULT_CONFIG = """\
{
    "github": {
        "id": 1,
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

random_secret = "".join(
    random.SystemRandom().choice(string.ascii_letters + string.digits)
    for _ in range(10)
)


def validate_cfg_json(value):
    """check that we have at least valid json and its a dict"""
    try:
        jv = json.loads(value)
    except ValueError as e:
        raise Invalid(
            _(
                "invalid_json",
                "JSON is not valid, parser complained: ${message}",
                mapping={"message": f"{e.msg} {e.pos}"},
            )
        )
    if not isinstance(jv, dict):
        raise Invalid(_("invalid_cfg_no_dict", "JSON root must be a mapping (dict)"))
    if len(jv) < 1:
        raise Invalid(
            _(
                "invalid_cfg_empty_dict",
                "At least one provider must be configured.",
            )
        )
    return True


@provider(IVocabularyFactory)
def userid_factory_vocabulary(context):
    items = []
    for name, factory in getUtilitiesFor(IUserIDFactory):
        items.append([factory.title, name])
    items = [SimpleTerm(name, name, title) for title, name in sorted(items)]
    return SimpleVocabulary(items)


class IPasPluginsAuthomaticSettings(Interface):

    secret = schema.TextLine(
        title=_("Secret"),
        description=_(
            "help_secret",
            default="Some random string used to encrypt the state",
        ),
        required=True,
        default=random_secret,
    )
    userid_factory_name = schema.Choice(
        vocabulary="pas.plugins.authomatic.userid_vocabulary",
        title=_("Generator for Plone User IDs."),
        description=_(
            "help_userid_factory_name",
            default="It is visible if no fullname is mapped and in some "
            "rare cases in URLs. It is the identifier used for "
            "the user inside Plone.",
        ),
        default="uuid",
    )
    json_config = schema.SourceText(
        title=_("JSON configuration"),
        description=_(
            "help_json_config",
            default="Configuration parameters for the different "
            "authorization providers. Details at "
            "https://authomatic.github.io/authomatic/reference/"
            "providers.html "
            '- difference: "class_" has to be a string, which is '
            "then resolved as a dotted path. Also sections "
            '"display" and "propertymap" are special.',
        ),
        required=True,
        constraint=validate_cfg_json,
        default=DEFAULT_CONFIG,
    )


class IAuthomaticPlugin(Interface):
    """Member Properties To Group Plugin"""

    def remember(result):
        """remember user as valid

        result is authomatic result data.
        """


class IUserIDFactory(Interface):
    """generates a userid on call"""

    def __call__(service_name, service_user_id, raw_user):
        """returns string, unique amongst plugins userids"""


class IPasPluginsAuthomaticLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
