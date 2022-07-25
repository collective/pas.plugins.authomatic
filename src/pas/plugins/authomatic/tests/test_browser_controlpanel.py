from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from pas.plugins.authomatic.testing import AUTHOMATIC_PLONE_FUNCTIONAL_TESTING
from pas.plugins.authomatic.testing import AUTHOMATIC_PLONE_INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.registry import Registry
from plone.testing.zope import Browser
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

import unittest


class TestAuthomaticSettingsControlPanel(unittest.TestCase):

    layer = AUTHOMATIC_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.registry = Registry()
        self.registry.registerInterface(IPasPluginsAuthomaticSettings)

    def test_authomatic_controlpanel_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name="authomatic-controlpanel"
        )
        # view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_authomatic_controlpanel_view_protected(self):
        from AccessControl import Unauthorized

        logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            "@@authomatic-controlpanel",
        )

    def test_authomatic_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            "authomatic"
            in [a.getAction(self)["id"] for a in self.controlpanel.listActions()]
        )

    def test_record_config_property(self):
        prefix = "pas.plugins.authomatic.interfaces"
        record_id = "IPasPluginsAuthomaticSettings.json_config"
        record = self.registry.records[f"{prefix}.{record_id}"]
        self.assertTrue("json_config" in IPasPluginsAuthomaticSettings)
        self.assertGreater(len(record.value), 20)


class ControlpanelFunctionalTest(unittest.TestCase):

    layer = AUTHOMATIC_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )

    def test_empty_form(self):
        self.browser.open("%s/authomatic-controlpanel" % self.portal_url)
        self.assertTrue(" Settings" in self.browser.contents)
