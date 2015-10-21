# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from pas.plugins.authomatic.interfaces import IAuthomaticPlugin
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS import interfaces as plonepas_interfaces
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from zope.interface import implementer
from pas.plugins.authomatic.utils import authomatic_cfg
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
    pas_interfaces.IAuthenticationPlugin,
    pas_interfaces.IPropertiesPlugin,
    pas_interfaces.ICredentialsUpdatePlugin
    # ... missing other auth plugins
)
class AuthomaticPlugin(BasePlugin):
    """Authomatic PAS Plugin
    """
    security = ClassSecurityInfo()
    meta_type = 'Authomatic Plugin'
    BasePlugin.manage_options

    # Tell PAS not to swallow our exceptions
    _dont_swallow_my_exceptions = False

    def __init__(self, id, title=None, **kw):
        self._setId(id)
        self.title = title
        self.plugin_caching = True
        self._users = OOBTree()

    # ##
    # pas_interfaces.IAuthenticationPlugin

    def authenticateCredentials(self, credentials):
        """ credentials -> (userid, login)

        - 'credentials' will be a mapping, as returned by IExtractionPlugin.
        - Return a  tuple consisting of user ID (which may be different
          from the login name) and login
        - If the credentials cannot be authenticated, return None.
        """
        login = credentials.get('login')
        token = credentials.get('password')
        if login not in self._users:
            return None
        if token != self._users[login]['token']:
            return None
        # XXX try to refresh token?
        return self._users[login]['userid'], login

    # ##
    # pas_interfaces.ICredentialsUpdatePlugin
    def updateCredentials(self, request, response, login, new_password):
        """ Callback:  user has changed her password.

        This interface is not responsible for the actual password change,
        it is used after a successful password change event.
        """
        if login not in self._users:
            return None
        self.users[login]['token'] = new_password

    # ##
    # pas_interfaces.plugins.IPropertiesPlugin

    # XXX security??

    def getPropertiesForUser(self, group, request=None):
        return None


InitializeClass(AuthomaticPlugin)
