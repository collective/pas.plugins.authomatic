# -*- coding: utf-8 -*-
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet

import unittest


class _MockRefresher(object):

    def refresh(*args):
        pass

_mock_refresher = _MockRefresher()


class TestPlugin(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def setUp(self):
        # create plugin
        from pas.plugins.authomatic.setuphandlers import _add_plugin
        self.aclu = self.layer['app'].acl_users
        _add_plugin(self.aclu, 'authomatic')
        self.plugin = self.aclu['authomatic']

    def test_authentication_empty_deny(self):
        credentials = {}
        result = self.plugin.authenticateCredentials(credentials)
        self.assertIsNone(result)

    def test_authentication_nonexistent_deny(self):
        credentials = {
            'login': 'UNSET',
            'password': 'UNSET',
        }
        result = self.plugin.authenticateCredentials(credentials)
        self.assertIsNone(result)

    def test_authentication_user_no_pass_deny(self):
        self.plugin._users['joe'] = {
            'userid': '123',
            'secret': 'UNSET',
        }
        credentials = {
            'login': 'joe',
            'password': 'SECRET',
        }
        result = self.plugin.authenticateCredentials(credentials)
        self.assertIsNone(result)

    def test_authentication_user_same_pass_allow(self):
        self.plugin._users['joe'] = {
            'userid': '123',
            'secret': 'SECRET',
            'credentials': _mock_refresher,
        }
        credentials = {
            'login': 'joe',
            'password': 'SECRET',
        }
        result = self.plugin.authenticateCredentials(credentials)
        self.assertEqual(result, ('123', 'joe'))

    def test_user_enumaration(self):
        self.plugin._users['joe'] = {
            'userid': '123joe',
            'secret': 'SECRET',
        }
        self.plugin._users['jane'] = {
            'userid': '123jane',
            'secret': 'SECRET',
        }
        self.plugin._users['wily'] = {
            'userid': '123wily',
            'secret': 'SECRET',
        }
        self.plugin._users['willi'] = {
            'userid': '123willi',
            'secret': 'SECRET',
        }
        # check by user id
        self.assertEqual(
            [{'login': 'joe', 'pluginid': 'authomatic', 'id': '123joe'}],
            self.plugin.enumerateUsers(id='123joe', exact_match=True)
        )
        self.assertEqual(
            [{'login': 'joe', 'pluginid': 'authomatic', 'id': '123joe'}],
            self.plugin.enumerateUsers(id='123joe')
        )
        self.assertEqual(
            4,
            len(self.plugin.enumerateUsers(id='123'))
        )
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(id='123j'))
        )

        # check by login
        self.assertEqual(
            [{'login': 'joe', 'pluginid': 'authomatic', 'id': '123joe'}],
            self.plugin.enumerateUsers(login='joe', exact_match=True)
        )
        self.assertEqual(
            [{'login': 'joe', 'pluginid': 'authomatic', 'id': '123joe'}],
            self.plugin.enumerateUsers(login='joe')
        )
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(login='j'))
        )
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(login='wil'))
        )
        # list all!
        self.assertEqual(
            4,
            len(self.plugin.enumerateUsers())
        )


class TestPropertyMapping(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def _make_provider(self, provider_name='Plone'):
        class MockProvider(object):
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

        return MockProvider(name=provider_name)

    def _make_one(self, data=None):
        from authomatic.core import User

        provider = self._make_provider()
        if not data:
            data = {
                u'displayName': u'Andrew Pipkin',
                u'domain': u'foobar.com',
                u'emails': [
                    {u'type': u'account', u'value': u'andrewpipkin@foobar.com'}
                ],
                u'etag': u'"xxxxxxxxxxxx/xxxxxxxxxxxx"',
                u'id': u'123456789',
                u'image': {
                    u'isDefault': False,
                    u'url': u'https://lh3.googleusercontent.com/photo.jpg'
                },
                u'isPlusUser': False,
                u'kind': u'plus#person',
                u'language': u'en_GB',
                u'name': {u'familyName': u'Pipkin', u'givenName': u'Andrew'},
                u'objectType': u'person',
                u'verified': False
            }
        user = User(provider)
        user.data = data
        user.id = u'123456789'
        user.username = u'andrewpipkin'
        user.name = u'Andrew Pipkin'
        user.first_name = u'Andrew'
        user.last_name = u'Pipkin'
        user.nickname = u'Andy'
        user.link = u'http://peterhudec.github.io/authomatic/'
        user.email = u'andrewpipkin@foobar.com'
        user.picture = u'https://lh3.googleusercontent.com/photo.jpg?sz=50'
        user.location = u'Innsbruck'
        return user

    def _make_propmap(self):
        return {
            'email': 'email',
            'link': 'home_page',
            'location': 'location',
            'name': 'fullname'
        }

    def setUp(self):
        # create plugin
        from pas.plugins.authomatic.setuphandlers import _add_plugin
        self.aclu = self.layer['app'].acl_users
        _add_plugin(self.aclu, 'authomatic')
        self.plugin = self.aclu['authomatic']

    def test_existing_user_attributes(self):
        user = self._make_one()
        propmap = self._make_propmap()
        result = self.plugin._make_sheet(user, propmap)
        self.assertIsInstance(result, UserPropertySheet)
        self.assertEqual(
            result.getProperty('home_page'),
            u'http://peterhudec.github.io/authomatic/'
        )
        self.assertEqual(result.getProperty('fullname'), u'Andrew Pipkin')
        self.assertEqual(
            result.getProperty('email'),
            u'andrewpipkin@foobar.com'
        )

    def test_provider_specific_user_attributes(self):
        user = self._make_one()
        propmap = self._make_propmap()
        propmap['data'] = {'domain': 'domain'}

        result = self.plugin._make_sheet(user, propmap)
        self.assertIsInstance(result, UserPropertySheet)
        self.assertEqual(
            result.getProperty('home_page'),
            u'http://peterhudec.github.io/authomatic/'
        )
        self.assertEqual(result.getProperty('fullname'), u'Andrew Pipkin')
        self.assertEqual(
            result.getProperty('email'),
            u'andrewpipkin@foobar.com'
        )
        self.assertEqual(result.getProperty('domain'), u'foobar.com')
