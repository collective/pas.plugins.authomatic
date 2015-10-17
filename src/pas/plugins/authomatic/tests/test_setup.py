# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_PLONE_INTEGRATION_TESTING  # noqa
from Products.CMFCore.utils import getToolByName

import unittest


class TestSetup(unittest.TestCase):
    """Test that pas.plugins.authomatic is properly installed."""

    layer = PAS_PLUGINS_Authomatic_PLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if pas.plugins.authomatic is installed with
           portal_quickinstaller.
        """
        self.assertTrue(
            self.installer.isProductInstalled(
                'pas.plugins.authomatic'
            )
        )
        self.assertIn('authomatic', self.portal.acl_users)

    def test_uninstall(self):
        """Test if pas.plugins.authomatic is cleanly uninstalled."""
        self.installer.uninstallProducts(['pas.plugins.authomatic'])
        self.assertFalse(
            self.installer.isProductInstalled(
                'pas.plugins.authomatic'
            )
        )
        # self.assertNotIn('authomatic', self.portal.acl_users)

    def test_browserlayer(self):
        """Test that IPasPluginsAuthomaticLayer is registered."""
        from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticLayer  # noqa
        from plone.browserlayer import utils
        self.assertTrue(
            IPasPluginsAuthomaticLayer in utils.registered_layers()
        )
