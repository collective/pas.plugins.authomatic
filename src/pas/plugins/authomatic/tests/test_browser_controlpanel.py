# -*- coding: utf-8 -*-
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings  # noqa
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_PLONE_INTEGRATION_TESTING  # noqa
from plone.app.testing import logout
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.registry import Registry
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

import unittest


class TestMailchimpSettingsControlPanel(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = Registry()
        self.registry.registerInterface(
            IPasPluginsAuthomaticSettings
        )

    def test_validator(self):
        from pas.plugins.authomatic.interfaces import validate_valid_groups  # noqa
        from zope.interface import Invalid
        with self.assertRaises(Invalid):
            validate_valid_groups(['1'])
        with self.assertRaises(Invalid):
            validate_valid_groups(['1|2|3|4|5|6'])

    def test_authomatic_controlpanel_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST),
            name="authomatic-controlpanel"
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_authomatic_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            '@@authomatic-controlpanel'
        )

    def test_authomatic_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'authomatic' in [
                a.getAction(self)['id']
                for a in self.controlpanel.listActions()
            ]
        )

    def test_record_group_property(self):
        record = self.registry.records[
            'pas.plugins.authomatic.interfaces.' +
            'IPasPluginsAuthomaticSettings.group_property'
        ]
        self.assertTrue(
            'group_property' in IPasPluginsAuthomaticSettings
        )
        self.assertEquals(record.value, u"")

    def test_record_valid_groups(self):
        record = self.registry.records[
            'pas.plugins.authomatic.interfaces.' +
            'IPasPluginsAuthomaticSettings.valid_groups'
        ]
        self.assertTrue(
            'valid_groups' in IPasPluginsAuthomaticSettings
        )
        self.assertEquals(record.value, [])


class ControlpanelFunctionalTest(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_PLONE_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

    def test_empty_form(self):
        self.browser.open(
            "%s/authomatic-controlpanel" % self.portal_url
        )
        self.assertTrue(
            "Member Properties To Group Settings" in self.browser.contents
        )
