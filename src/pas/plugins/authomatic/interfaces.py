from pas.plugins.authomatic import _
from pas.plugins.authomatic import config
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPasPluginsAuthomaticSettings(Interface):
    secret = schema.TextLine(
        title=_("Secret"),
        description=_(
            "help_secret",
            default="Some random string used to encrypt the state",
        ),
        required=True,
        default=config.random_secret,
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
        default="username_userid",
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
        constraint=config.validate_cfg_json,
        default=config.DEFAULT_CONFIG,
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
