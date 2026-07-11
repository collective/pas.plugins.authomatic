from pas.plugins.authomatic.config import DEFAULT_ID
from pas.plugins.authomatic.plugin import AuthomaticPlugin
from plone import api
from plone.base.interfaces import INonInstallable
from Products.GenericSetup.tool import SetupTool
from Products.PluggableAuthService.PluggableAuthService import PluggableAuthService
from zope.interface import implementer


TITLE = "Authomatic OAuth plugin (pas.plugins.authomatic)"


def _add_plugin(pas: PluggableAuthService, pluginid: str = DEFAULT_ID):
    if pluginid in pas.objectIds():
        return f"{TITLE} already installed."
    if pluginid != DEFAULT_ID:
        return f"ID of plugin must be {DEFAULT_ID}"
    plugin = AuthomaticPlugin(pluginid, title=TITLE)
    pas._setObject(pluginid, plugin)
    plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
    for info in pas.plugins.listPluginTypeInfo():
        interface = info["interface"]
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface,
            [x[0] for x in pas.plugins.listPlugins(interface)[:-1]],
        )


def _remove_plugin(pas: PluggableAuthService, pluginid: str = DEFAULT_ID):
    if pluginid in pas.objectIds():
        pas.manage_delObjects([pluginid])


def post_install(context: SetupTool):
    acl_users = api.portal.get_tool("acl_users")
    _add_plugin(acl_users)


def post_uninstall(context: SetupTool):
    acl_users = api.portal.get_tool("acl_users")
    _remove_plugin(acl_users)


@implementer(INonInstallable)
class HiddenProfiles:
    """Hidden profiles for this package."""

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            "pas.plugins.authomatic:uninstall",
        ]
