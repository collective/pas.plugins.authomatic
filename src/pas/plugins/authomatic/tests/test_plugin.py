# -*- coding: utf-8 -*-
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
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
