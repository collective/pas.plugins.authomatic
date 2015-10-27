# -*- coding: utf-8 -*-
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
import mock
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
        self.plugin._users['joe'] = {
            'userid': '123',
            'token': 'UNSET',
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
            'token': 'SECRET',
        }
        credentials = {
            'login': 'joe',
            'password': 'SECRET',
        }
        result = self.plugin.authenticateCredentials(credentials)
        self.assertEqual(result, ('123', 'joe'))

