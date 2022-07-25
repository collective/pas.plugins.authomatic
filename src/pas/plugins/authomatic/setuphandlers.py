from pas.plugins.authomatic.interfaces import DEFAULT_ID
from pas.plugins.authomatic.plugin import AuthomaticPlugin
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


TITLE = "Authomatic OAuth plugin (pas.plugins.authomatic)"


def _add_plugin(pas, pluginid=DEFAULT_ID):
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


def _remove_plugin(pas, pluginid=DEFAULT_ID):
    if pluginid in pas.objectIds():
        pas.manage_delObjects([pluginid])


def post_install(context):
    _add_plugin(context.aq_parent.acl_users)


def post_uninstall(context):
    _remove_plugin(context.aq_parent.acl_users)


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            "pas.plugins.authomatic:uninstall",
        ]
