# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from operator import itemgetter
from pas.plugins.authomatic.interfaces import IAuthomaticPlugin
from pas.plugins.authomatic.useridentities import UserIdentities
from pas.plugins.authomatic.useridfactories import new_userid
from plone import api
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.interfaces.authservice import _noroles
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.interface import implementer
import logging
import os

logger = logging.getLogger(__name__)
tpl_dir = os.path.join(os.path.dirname(__file__), 'browser')

_marker = {}


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
    pas_interfaces.IUserEnumerationPlugin,
)
class AuthomaticPlugin(BasePlugin):
    """Authomatic PAS Plugin
    """
    security = ClassSecurityInfo()
    meta_type = 'Authomatic Plugin'
    BasePlugin.manage_options

    # Tell PAS not to swallow our exceptions
    _dont_swallow_my_exceptions = True

    def __init__(self, id, title=None, **kw):
        self._setId(id)
        self.title = title
        self.plugin_caching = True
        self._init_trees()

    def _init_trees(self):
        # (provider_name, provider_userid) -> userid
        self._userid_by_identityinfo = OOBTree()

        # userid -> userdata
        self._useridentities_by_userid = OOBTree()

    def _provider_id(self, result):
        """helper to get the provider identifier
        """
        if not result.user.id:
            raise ValueError('Invalid: Empty user.id')
        if not result.provider.name:
            raise ValueError('Invalid: Empty provider.name')
        return (result.provider.name, result.user.id)

    @security.private
    def lookup_identities(self, result):
        """looks up the UserIdentities by using the provider name and the
        userid at this provider
        """
        userid = self._userid_by_identityinfo.get(
            self._provider_id(result),
            None
        )
        return self._useridentities_by_userid.get(userid, None)

    @security.private
    def remember_identity(self, result, userid=None):
        """stores authomatic result data
        """
        if userid is None:
            # create a new userid
            userid = new_userid(self, result)
            useridentities = UserIdentities(userid)
            self._useridentities_by_userid[userid] = useridentities
        else:
            # use existing userid
            useridentities = self._useridentities_by_userid.get(userid, None)
            if useridentities is None:
                raise ValueError('Invalid userid')
        provider_id = self._provider_id(result)
        if provider_id not in self._userid_by_identityinfo:
            self._userid_by_identityinfo[provider_id] = userid

        useridentities.handle_result(result)
        return useridentities

    @security.private
    def remember(self, result):
        """remember user as valid

        result is authomatic result data.
        """
        # first fetch provider specific user-data
        result.user.update()

        # lookup user by
        useridentities = self.lookup_identities(result)
        if useridentities is None:
            # new/unknown user
            useridentities = self.remember_identity(result)
            logger.info('New User: {0}'.format(useridentities.userid))
        else:
            useridentities.update_userdata(result)
            logger.info('Updated Userdata: {0}'.format(useridentities.userid))

        # login (get new security manager)
        logger.info('Login User: {0}'.format(useridentities.userid))
        aclu = api.portal.get_tool('acl_users')
        user = aclu._findUser(aclu.plugins, useridentities.userid)
        accessed, container, name, value = aclu._getObjectContext(
            self.REQUEST['PUBLISHED'],
            self.REQUEST
        )
        user = aclu._authorizeUser(
            user,
            accessed,
            container,
            name,
            value,
            _noroles
        )

        # do login post-processing
        self.REQUEST['__ac_password'] = useridentities.secret
        mt = api.portal.get_tool('portal_membership')
        logger.info('Login Postprocessing: {0}'.format(useridentities.userid))
        mt.loginUser(self.REQUEST)

    # ##
    # pas_interfaces.IAuthenticationPlugin

    @security.public
    def authenticateCredentials(self, credentials):
        """ credentials -> (userid, login)

        - 'credentials' will be a mapping, as returned by IExtractionPlugin.
        - Return a  tuple consisting of user ID (which may be different
          from the login name) and login
        - If the credentials cannot be authenticated, return None.
        """
        login = credentials.get('login', None)
        password = credentials.get('password', None)
        if not login or login not in self._useridentities_by_userid:
            return None
        identities = self._useridentities_by_userid[login]
        if identities.check_password(password):
            return login, login

    # ##
    # pas_interfaces.plugins.IPropertiesPlugin

    @security.private
    def getPropertiesForUser(self, user, request=None):
        identity = self._useridentities_by_userid.get(
            user.getId(),
            _marker
        )
        if identity is _marker:
            return None
        return identity.propertysheet

    # ##
    # pas_interfaces.plugins.IUserEnumaration

    @security.private
    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        """-> ( user_info_1, ... user_info_N )

        o Return mappings for users matching the given criteria.

        o 'id' or 'login', in combination with 'exact_match' true, will
          return at most one mapping per supplied ID ('id' and 'login'
          may be sequences).

        o If 'exact_match' is False, then 'id' and / or login may be
          treated by the plugin as "contains" searches (more complicated
          searches may be supported by some plugins using other keyword
          arguments).

        o If 'sort_by' is passed, the results will be sorted accordingly.
          known valid values are 'id' and 'login' (some plugins may support
          others).

        o If 'max_results' is specified, it must be a positive integer,
          limiting the number of returned mappings.  If unspecified, the
          plugin should return mappings for all users satisfying the criteria.

        o Minimal keys in the returned mappings:

          'id' -- (required) the user ID, which may be different than
                  the login name

          'login' -- (required) the login name

          'pluginid' -- (required) the plugin ID (as returned by getId())

          'editurl' -- (optional) the URL to a page for updating the
                       mapping's user

        o Plugin *must* ignore unknown criteria.

        o Plugin may raise ValueError for invalid criteria.

        o Insufficiently-specified criteria may have catastrophic
          scaling issues for some implementations.
        """
        if id and login and id != login:
            raise ValueError('plugin does not support id different from login')
        search_id = id or login
        if search_id:
            if not isinstance(search_id, basestring):
                raise NotImplementedError('sequence is not supported.')
        else:
            return ()

        pluginid = self.getId()
        ret = list()
        # shortcut for exact match of login/id
        identity = None
        if (
            exact_match and
            search_id and
            search_id in self._useridentities_by_userid
        ):
            identity = self._useridentities_by_userid[search_id]
        if identity is not None:
            ret.append({
                'id': identity.userid.encode('utf8'),
                'login': identity.userid.encode('utf8'),
                'pluginid': pluginid
            })
            return ret

        # non exact expensive search
        for userid in self._useridentities_by_userid:
            if not userid:
                logger.warn('None userid found. This should not happen!')
                continue
            if not userid.startswith(search_id):
                continue
            identity = self._useridentities_by_userid[userid]
            ret.append({
                'id': identity.userid.decode('utf8'),
                'login': identity.userid,
                'pluginid': pluginid
            })
            if max_results and len(ret) >= max_results:
                break
        if sort_by in ['id', 'login']:
            return sorted(ret, key=itemgetter(sort_by))
        return ret


InitializeClass(AuthomaticPlugin)
