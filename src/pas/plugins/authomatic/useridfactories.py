# -*- coding: utf-8 -*-
from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.interfaces import IUserIDFactory
from pas.plugins.authomatic.utils import authomatic_settings
from zope.component import queryUtility
from zope.interface import implementer
import uuid


@implementer(IUserIDFactory)
class BaseUserIDFactory(object):

    def normalize(self, plugin, result, userid):
        new_userid = userid
        counter = 2  # first was taken, so logically its second
        while new_userid in plugin._useridentities_by_userid:
            new_userid = '{0}_{1}'.format(userid, counter)
            counter += 1
        return new_userid


class UUID4UserIDFactory(BaseUserIDFactory):

    title = _(u'UUID as User ID')

    def __call__(self, plugin, result):
        return self.normalize(plugin, result, str(uuid.uuid4()))


class ProviderIDUserIDFactory(BaseUserIDFactory):

    title = _(u'Provider User ID')

    def __call__(self, plugin, result):
        return self.normalize(plugin, result, result.user.id)


class ProviderIDUserNameFactory(BaseUserIDFactory):

    title = _(u'Provider Login')

    def __call__(self, plugin, result):
        return self.normalize(plugin, result, result.user.login)


def new_userid(plugin, result):
    settings = authomatic_settings()
    factory = queryUtility(
        IUserIDFactory,
        name=settings.userid_factory_name,
        default=UUID4UserIDFactory()
    )
    return factory(plugin, result)
