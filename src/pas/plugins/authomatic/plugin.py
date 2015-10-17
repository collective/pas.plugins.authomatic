# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from pas.plugins.authomatic.interfaces import IAuthomaticPlugin
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings  # noqa
from plone.registry.interfaces import IRegistry
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS import interfaces as plonepas_interfaces
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from zope.component import queryUtility
from zope.interface import implementer
import logging
import os

logger = logging.getLogger(__name__)
tpl_dir = os.path.join(os.path.dirname(__file__), 'browser')


def manage_addAuthomaticPlugin(context, id, title='', RESPONSE=None, **kw):
    """Create an instance of a Authomatic Plugin.
    """
    plugin = AuthomaticPlugin(id, title, **kw)
    context._setObject(plugin.getId(), plugin)
    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')


manage_addAuthomaticPluginForm = PageTemplateFile(
    os.path.join(tpl_dir, 'add_plugin.pt'),
    globals(),
    __name__='addAuthomaticPlugin'
)


@implementer(
    IAuthomaticPlugin,
    pas_interfaces.IPropertiesPlugin,
    # ... missing other auth plugins
)
class AuthomaticPlugin(BasePlugin):
    """Memberproperties to Group mapping PAS plugin
    """
    # using implements explicit here for python 2.4 compat.
    security = ClassSecurityInfo()
    meta_type = 'Authomatic Plugin'
    BasePlugin.manage_options

    # Tell PAS not to swallow our exceptions
    _dont_swallow_my_exceptions = False

    def __init__(self, id, title=None, **kw):
        self._setId(id)
        self.title = title
        self.plugin_caching = True

    # ##
    # helper

    @property
    def _settings(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(
            IPasPluginsAuthomaticSettings,
        )
        return settings

    # ##
    # pas_interfaces.plugins.IPropertiesPlugin

    # XXX security??

    def getPropertiesForUser(self, group, request=None):
        return None


InitializeClass(AuthomaticPlugin)
