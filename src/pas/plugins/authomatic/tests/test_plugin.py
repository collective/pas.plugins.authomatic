# -*- coding: utf-8 -*-
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
import mock
import unittest


class TestPluginHelpers(unittest.TestCase):
    """check if helpers work
    """

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def setUp(self):
        """Custom shared utility setup for tests."""
        # create plugin
        from pas.plugins.authomatic.plugin import manage_addAuthomaticPlugin
        self.aclu = self.layer['app'].acl_users
        manage_addAuthomaticPlugin(self.aclu, 'authomatic')
        self.plugin = self.aclu['authomatic']

    def test_pass(self):
        pass


class TestPlugin(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def setUp(self):
        # create plugin
        from pas.plugins.authomatic.setuphandlers import _add_plugin
        self.aclu = self.layer['app'].acl_users
        _add_plugin(self.aclu, 'authomatic')
        self.plugin = self.aclu['authomatic']

    def test_pass(self):
        pass
