# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from pas.plugins.authomatic.interfaces import IAuthomaticPlugin
from pas.plugins.authomatic.utils import authomatic_cfg
from persistent.dict import PersistentDict
from plone import api
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.interfaces.authservice import _noroles
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from zope.interface import implementer
import logging
import os
import uuid

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
        self._users = OOBTree()

    def _make_sheet(self, user, propmap):
        pdata = dict(id=user.id)
        user_dict = user.to_dict()

        for akey, pkey in propmap.items():
            # Always search first on the user attributes, then on the raw data
            # this guaratees we do not break existing configurations
            ainfo = user_dict.get(akey, user_dict['data'].get(akey, None))
            if ainfo is not None:
                if isinstance(pkey, dict):
                    for k, v in pkey.items():
                        pdata[k] = ainfo.get(v)
                else:
                    pdata[pkey] = ainfo

        sheet = UserPropertySheet(**pdata)
        return sheet

    @security.private
    def remember(self, result):
        """remember user as valid

        result is authomatic result data.
        """
        # first fetch service specific user-data
        result.user.update()
        login = result.user.id
        userid = result.user.id

        if login not in self._users:
            # collect data
            data = PersistentDict()
            data['secret'] = str(uuid.uuid4())
            data['userid'] = userid  # XXX maybe something else
        else:
            data = self._users[login]

        cfg = authomatic_cfg()
        provider_cfg = cfg[result.provider.name]
        propmap = provider_cfg.get('propertymap', {})
        data['sheet'] = self._make_sheet(result.user, propmap)
        data['credentials'] = result.user.credentials
        self._users[login] = data

        # login (get new security manager)
        aclu = api.portal.get_tool('acl_users')
        user = aclu._findUser(aclu.plugins, data['userid'])
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
        self.REQUEST['__ac_password'] = data['secret']
        mt = api.portal.get_tool('portal_membership')
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
        if not login or login not in self._users:
            return None
        if password != self._users[login].get('secret', _marker):
            return None

        # this delegates refresh to authomatic
        rf_credentials = self._users[login]['credentials'].refresh()
        if rf_credentials is not None:
            # refreshed, happens rarely
            self._users[login]['credentials'] = credentials

            # XXX need to check if login was still valid
            # eventually invalidate users credentials if so.
            # and return None

        # ok
        return self._users[login]['userid'], login

    # ##
    # pas_interfaces.plugins.IPropertiesPlugin
    # XXX security??

    def getPropertiesForUser(self, user, request=None):
        data = self._users.get(user.getId(), _marker)
        if data is _marker:
            return None
        return data['sheet']

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
        search_id = id
        if login:
            if not isinstance(login, basestring):
                # XXX TODO
                raise NotImplementedError('sequence is not supported yet.')
            kw['login'] = login

        # pas search users gives both login and name if login is meant
        if "login" in kw and "name" in kw:
            del kw["name"]

        if search_id:
            if not isinstance(search_id, basestring):
                raise NotImplementedError('sequence is not supported yet.')
            kw['id'] = search_id
        pluginid = self.getId()
        ret = list()
        for login_entry in self._users:
            data = self._users[login_entry]
            if exact_match:
                if search_id and data['userid'] != search_id:
                    continue
                if login and login_entry != login:
                    continue
            else:
                if search_id and not data['userid'].startswith(search_id):
                    continue
                if login and not login_entry.startswith(login):
                    continue
            ret.append({
                'id': data['userid'].encode('utf8'),
                'login': login_entry,
                'pluginid': pluginid}
            )
        if max_results and len(ret) > max_results:
            ret = ret[:max_results]
        return ret


InitializeClass(AuthomaticPlugin)
