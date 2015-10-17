# -*- coding: utf-8 -*-
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE  # noqa

import unittest


class TestPluginForGroupCapability(unittest.TestCase):
    """interface plonepas_interfaces.capabilities.IGroupCapability

    Test if above interface works as expected
    """

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.aclu = self.layer['app'].acl_users

    def test_addplugin(self):
        PLUGINID = 'authomatic'
        from pas.plugins.authomatic.setuphandlers import _add_plugin
        result = _add_plugin(self.aclu, pluginid=PLUGINID)
        self.assertIs(result, None)
        self.assertIn(PLUGINID, self.aclu.objectIds())

        from pas.plugins.authomatic.plugin import AuthomaticPlugin
        authomatic = self.aclu[PLUGINID]
        self.assertIsInstance(authomatic, AuthomaticPlugin)

        from pas.plugins.authomatic.setuphandlers import TITLE
        result = _add_plugin(self.aclu, pluginid=PLUGINID)
        self.assertEqual(result, TITLE + ' already installed.')

    def test_removeplugin(self):
        # add before remove
        PLUGINID = 'authomatic'
        from pas.plugins.authomatic.setuphandlers import _add_plugin
        _add_plugin(self.aclu, pluginid=PLUGINID)
        self.assertIn(PLUGINID, self.aclu.objectIds())

        # now remove it
        from pas.plugins.authomatic.setuphandlers import _remove_plugin  # noqa
        _remove_plugin(self.aclu, pluginid=PLUGINID)
        self.assertNotIn(PLUGINID, self.aclu.objectIds())
