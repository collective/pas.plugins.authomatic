from .plugin import authomatic_plugin
from pas.plugins.authomatic import _types as t
from pas.plugins.authomatic.useridentities import UserIdentities
from pathlib import Path
from plone.restapi.serializer.converters import json_compatible
from typing import Any

import json


DEFAULT_DELIMITER = "|"


def _useridentities_as_dict(identities: UserIdentities) -> dict[str, Any]:
    """Serialize a :class:`UserIdentities` instance to a plain dict.

    :param identities: The user identities to serialize.
    :returns: A JSON-serializable mapping of the stored identities.
    """
    data = {
        "userid": identities.userid,
        "secret": identities.secret,
        "identities": {
            provider: dict(identity)
            for provider, identity in identities._identities.items()
        },
    }
    # No ``context``: identity data is plain values, so the context-free
    # ``IJsonCompatible`` path applies. Passing a ``context`` would route to
    # ``IContextawareJsonCompatible``, which has no adapter for plain dicts
    # and would silently return ``None``.
    serialized_data: dict[str, Any] = json_compatible(data)
    return serialized_data


def _get_plugindata(delimiter: str = DEFAULT_DELIMITER) -> t.SerializedPluginData:
    """Serialize the Authomatic plugin state.

    :param delimiter: Separator used to join each ``(provider_name,
        provider_id)`` identity-info key into a single string.
    :returns: The serialized plugin state (empty when no plugin is available).
    """
    userid_by_identityinfo: dict[str, str] = {}
    useridentities_by_userid: dict[str, dict[str, Any]] = {}
    if plugin := authomatic_plugin():
        userid_by_identityinfo = {
            f"{provider_name}{delimiter}{provider_id}": userid
            for (
                provider_name,
                provider_id,
            ), userid in plugin._userid_by_identityinfo.items()
        }
        useridentities_by_userid = {
            userid: _useridentities_as_dict(identities)
            for userid, identities in plugin._useridentities_by_userid.items()
        }
    return {
        "userid_by_identityinfo": userid_by_identityinfo,
        "useridentities_by_userid": useridentities_by_userid,
    }


def _set_plugindata(
    data: t.SerializedPluginData, delimiter: str = DEFAULT_DELIMITER
) -> bool:
    """Restore the Authomatic plugin state from serialized data.

    :param data: Serialized plugin state produced by :func:`_get_plugindata`.
    :param delimiter: Separator used to split the identity-info keys back into
        ``(provider_name, provider_id)`` tuples.
    :returns: ``True`` when the data was imported, ``False`` when no Authomatic
        plugin is available.
    """
    status = False
    if plugin := authomatic_plugin():
        for key, userid in data["userid_by_identityinfo"].items():
            provider_name, provider_id = key.split(delimiter, 1)
            plugin._userid_by_identityinfo[(provider_name, provider_id)] = userid
        for userid, identities_data in data["useridentities_by_userid"].items():
            plugin._useridentities_by_userid[userid] = UserIdentities.from_dict(
                identities_data
            )
        status = True
    return status


def export_plugin_data(path: Path, delimiter: str = DEFAULT_DELIMITER) -> Path:
    """Export the plugin's user identities to a JSON file.

    :param path: Destination file for the JSON export.
    :param delimiter: Separator used for the identity-info keys.
    :returns: The path the data was written to.
    """
    data = _get_plugindata(delimiter=delimiter)
    path.write_text(json.dumps(data, indent=2))
    return path


def import_plugin_data(path: Path, delimiter: str = DEFAULT_DELIMITER) -> bool:
    """Import user identities into the plugin from a JSON file.

    :param path: JSON file previously written by :func:`export_plugin_data`.
    :param delimiter: Separator used for the identity-info keys.
    :returns: ``True`` when the data was imported, ``False`` when no Authomatic
        plugin is available.
    """
    data = json.loads(path.read_text())
    return _set_plugindata(data, delimiter=delimiter)
