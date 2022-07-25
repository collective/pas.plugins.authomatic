from AccessControl.Permissions import add_user_folders
from pas.plugins.authomatic.plugin import AuthomaticPlugin
from pas.plugins.authomatic.plugin import manage_addAuthomaticPlugin
from pas.plugins.authomatic.plugin import manage_addAuthomaticPluginForm
from pas.plugins.authomatic.plugin import tpl_dir
from Products.PluggableAuthService import registerMultiPlugin


def initialize(context):
    """Initializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.
    """
    registerMultiPlugin(AuthomaticPlugin.meta_type)
    context.registerClass(
        AuthomaticPlugin,
        permission=add_user_folders,
        icon=tpl_dir / "authomatic.png",
        constructors=(manage_addAuthomaticPluginForm, manage_addAuthomaticPlugin),
        visibility=None,
    )
