from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from operator import itemgetter
from pas.plugins.authomatic.interfaces import IAuthomaticPlugin
from pas.plugins.authomatic.useridentities import UserIdentities
from pas.plugins.authomatic.useridfactories import new_userid
from pathlib import Path
from plone import api
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.interfaces.capabilities import IDeleteCapability
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PluggableAuthService.events import PrincipalCreated
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.interfaces.authservice import _noroles
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import createViewName
from zope.event import notify
from zope.interface import implementer

import logging


logger = logging.getLogger(__name__)
tpl_dir = Path(__file__).parent.resolve() / "browser"

_marker = {}


def manage_addAuthomaticPlugin(context, id, title="", RESPONSE=None, **kw):
    """Create an instance of a Authomatic Plugin."""
    plugin = AuthomaticPlugin(id, title, **kw)
    context._setObject(plugin.getId(), plugin)
    if RESPONSE is not None:
        RESPONSE.redirect("manage_workspace")


manage_addAuthomaticPluginForm = PageTemplateFile(
    tpl_dir / "add_plugin.pt",
    globals(),
    __name__="addAuthomaticPlugin",
)


@implementer(
    IAuthomaticPlugin,
    pas_interfaces.IAuthenticationPlugin,
    pas_interfaces.IPropertiesPlugin,
    pas_interfaces.IUserEnumerationPlugin,
    IUserManagement,
    IDeleteCapability,
)
class AuthomaticPlugin(BasePlugin):
    """Authomatic PAS Plugin"""

    security = ClassSecurityInfo()
    meta_type = "Authomatic Plugin"
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
        """helper to get the provider identifier"""
        if not result.user.id:
            raise ValueError("Invalid: Empty user.id")
        if not result.provider.name:
            raise ValueError("Invalid: Empty provider.name")
        return (result.provider.name, result.user.id)

    @security.private
    def lookup_identities(self, result):
        """looks up the UserIdentities by using the provider name and the
        userid at this provider
        """
        userid = self._userid_by_identityinfo.get(self._provider_id(result), None)
        return self._useridentities_by_userid.get(userid, None)

    @security.private
    def remember_identity(self, result, userid=None):
        """stores authomatic result data"""
        if userid is None:
            # create a new userid
            userid = new_userid(self, result)
            useridentities = UserIdentities(userid)
            self._useridentities_by_userid[userid] = useridentities
        else:
            # use existing userid
            useridentities = self._useridentities_by_userid.get(userid, None)
            if useridentities is None:
                raise ValueError("Invalid userid")
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

        do_notify_created = False

        # lookup user by
        useridentities = self.lookup_identities(result)
        if useridentities is None:
            # new/unknown user
            useridentities = self.remember_identity(result)
            do_notify_created = True
            logger.info(f"New User: {useridentities.userid}")
        else:
            useridentities.update_userdata(result)
            logger.info(f"Updated Userdata: {useridentities.userid}")

        # login (get new security manager)
        logger.info(f"Login User: {useridentities.userid}")
        aclu = api.portal.get_tool("acl_users")
        user = aclu._findUser(aclu.plugins, useridentities.userid)
        accessed, container, name, value = aclu._getObjectContext(
            self.REQUEST["PUBLISHED"], self.REQUEST
        )
        # Add the user to the SM stack
        aclu._authorizeUser(user, accessed, container, name, value, _noroles)
        if do_notify_created:
            # be a good citizen in PAS world and notify user creation
            notify(PrincipalCreated(user))

        # do login post-processing
        self.REQUEST["__ac_password"] = useridentities.secret
        mt = api.portal.get_tool("portal_membership")
        logger.info(f"Login Postprocessing: {useridentities.userid}")
        mt.loginUser(self.REQUEST)

    # ##
    # pas_interfaces.IAuthenticationPlugin

    @security.public
    def authenticateCredentials(self, credentials):
        """credentials -> (userid, login)

        - 'credentials' will be a mapping, as returned by IExtractionPlugin.
        - Return a  tuple consisting of user ID (which may be different
          from the login name) and login
        - If the credentials cannot be authenticated, return None.
        """
        login = credentials.get("login", None)
        password = credentials.get("password", None)
        if not login or login not in self._useridentities_by_userid:
            return None
        identities = self._useridentities_by_userid[login]
        if identities.check_password(password):
            return login, login

    # ##
    # pas_interfaces.plugins.IPropertiesPlugin

    @security.private
    def getPropertiesForUser(self, user, request=None):
        identity = self._useridentities_by_userid.get(user.getId(), _marker)
        if identity is _marker:
            return None
        return identity.propertysheet

    # ##
    # pas_interfaces.plugins.IUserEnumaration

    @security.private
    def enumerateUsers(
        self,
        id=None,
        login=None,
        exact_match=False,
        sort_by=None,
        max_results=None,
        **kw,
    ):
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
            raise ValueError("plugin does not support id different from login")
        search_id = id or login
        if not search_id:
            return ()
        if not isinstance(search_id, str):
            raise NotImplementedError("sequence is not supported.")

        pluginid = self.getId()
        ret = list()
        # shortcut for exact match of login/id
        identity = None
        if exact_match and search_id and search_id in self._useridentities_by_userid:
            identity = self._useridentities_by_userid[search_id]
        if identity is not None:
            userid = identity.userid
            ret.append({"id": userid, "login": userid, "pluginid": pluginid})
            return ret

        if exact_match:
            # we're claiming an exact match search, if we still don't
            # have anything, better bail.
            return ret

        # non exact expensive search
        for userid in self._useridentities_by_userid:
            if not userid:
                logger.warn("None userid found. This should not happen!")
                continue

            # search for a match in fullname, email and userid
            identity = self._useridentities_by_userid[userid]
            search_term = search_id.lower()
            identity_userid = identity.userid
            identity_fullname = identity.propertysheet.getProperty(
                "fullname", ""
            ).lower()
            identity_email = identity.propertysheet.getProperty("email", "").lower()
            if (
                search_term not in identity_userid
                and search_term not in identity_fullname  # noqa: W503
                and search_term not in identity_email  # noqa: W503
            ):
                continue

            #            if not userid.startswith(search_id):
            #                continue
            #            identity = self._useridentities_by_userid[userid]
            #            identity_userid = identity.userid
            ret.append(
                {
                    "id": identity_userid,
                    "login": identity.userid,
                    "pluginid": pluginid,
                }
            )
            if max_results and len(ret) >= max_results:
                break
        if sort_by in ["id", "login"]:
            return sorted(ret, key=itemgetter(sort_by))
        return ret

    @security.public
    def allowDeletePrincipal(self, principal_id):
        """True if this plugin can delete a certain user/group.
        This is true if this plugin manages the user.
        """
        return principal_id in self._useridentities_by_userid

    @security.private
    def doDeleteUser(self, userid):
        """Given a user id, delete that user"""
        return self.removeUser(userid)

    @security.private
    def doChangeUser(self, userid, password=None, **kw):
        """do nothing"""
        return False

    @security.private
    def doAddUser(self, login, password):
        """do nothing"""
        return False

    @security.private
    def getPluginIdByUserId(self, user_id):
        """
        return the right key for given user_id
        """
        for k, v in self._userid_by_identityinfo.items():
            if v == user_id:
                return k
        return ""

    @security.private
    def removeUser(self, user_id):
        """ """
        # Remove the user from all persistent dicts
        if user_id not in self._useridentities_by_userid:
            # invalid userid
            return
        del self._useridentities_by_userid[user_id]

        plugin_id = self.getPluginIdByUserId(user_id)
        if plugin_id:
            del self._userid_by_identityinfo[plugin_id]
        # Also, remove from the cache
        view_name = createViewName("enumerateUsers")
        self.ZCacheable_invalidate(view_name=view_name)
        view_name = createViewName("enumerateUsers", user_id)
        self.ZCacheable_invalidate(view_name=view_name)


InitializeClass(AuthomaticPlugin)
