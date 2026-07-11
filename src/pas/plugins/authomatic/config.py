"""Package constants and configuration helpers.

This is a dependency-light leaf module: it must not import from
:mod:`pas.plugins.authomatic.interfaces` (or anything that imports it) so it
can be safely imported by both ``interfaces`` and ``utils``.
"""

from pas.plugins.authomatic import _
from zope.interface import Invalid

import json
import random
import string


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


def validate_cfg_json(value: str) -> bool:
    """Check that we have at least valid json and it is a dict.

    :param value: JSON configuration to validate.
    :returns: ``True`` when the configuration is valid.
    :raises Invalid: when the configuration is not a non-empty JSON mapping.
    """
    try:
        jv = json.loads(value)
    except json.JSONDecodeError as e:
        raise Invalid(
            _(
                "invalid_json",
                "JSON is not valid, parser complained: ${message}",
                mapping={"message": f"{e.msg} {e.pos}"},
            )
        ) from None
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
