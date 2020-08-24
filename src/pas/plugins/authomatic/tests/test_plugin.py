# -*- coding: utf-8 -*-
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
from pas.plugins.authomatic.tests.mocks import make_user

import unittest


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
        make_user('joe', testcase=self)
        credentials = {
            'login': 'joe',
            'password': 'SECRET',
        }
        result = self.plugin.authenticateCredentials(credentials)
        self.assertIsNone(result)

    def test_authentication_user_same_pass_allow(self):
        make_user('joe', testcase=self, password='SECRET')
        credentials = {
            'login': 'joe',
            'password': 'SECRET'
        }
        result = self.plugin.authenticateCredentials(credentials)
        self.assertEqual(result, ('joe', 'joe'))

    def test_user_enumaration(self):
        make_user('123joe', testcase=self)
        make_user('123jane', testcase=self)
        make_user('123wily', testcase=self)
        make_user('123willi', testcase=self)
        # check by user id
        self.assertEqual(
            [{'login': '123joe', 'pluginid': 'authomatic', 'id': '123joe'}],
            self.plugin.enumerateUsers(id='123joe', exact_match=True)
        )
        self.assertEqual(
            [{'login': '123joe', 'pluginid': 'authomatic', 'id': '123joe'}],
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
            [{'login': '123joe', 'pluginid': 'authomatic', 'id': '123joe'}],
            self.plugin.enumerateUsers(login='123joe', exact_match=True)
        )
        self.assertEqual(
            [{'login': '123joe', 'pluginid': 'authomatic', 'id': '123joe'}],
            self.plugin.enumerateUsers(login='123joe')
        )
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(login='123j'))
        )
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(login='123wil'))
        )
        # https://github.com/collective/pas.plugins.authomatic/pull/25/commits/5c0f6b1dc76a0d769e35a845ce4c4dd4307655ba
        # Due to the workarround, now the enumerateUsers plugin doesn't return
        # any users when searching with an empty query
        self.assertEqual(
            0,
            len(self.plugin.enumerateUsers())
        )

    def test_user_delete(self):
        make_user('123joe', testcase=self)
        make_user('123jane', testcase=self)
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(login='123j'))
        )
        self.assertEqual(
            1,
            len(self.plugin.enumerateUsers(login='123joe'))
        )
        self.plugin.doDeleteUser(userid="123joe")
        self.assertEqual(
            1,
            len(self.plugin.enumerateUsers(login='123j'))
        )
        self.assertEqual(
            0,
            len(self.plugin.enumerateUsers(login='123joe'))
        )

    def test_user_delete_invalid_uid(self):
        make_user('123joe', testcase=self)
        make_user('123jane', testcase=self)
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(login='123j'))
        )
        self.assertEqual(
            1,
            len(self.plugin.enumerateUsers(login='123joe'))
        )
        self.plugin.doDeleteUser(userid="123foo")
        self.assertEqual(
            2,
            len(self.plugin.enumerateUsers(login='123j'))
        )
