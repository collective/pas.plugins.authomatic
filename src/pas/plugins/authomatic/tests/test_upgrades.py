"""Upgrades tests for this package."""
from parameterized import parameterized
from pas.plugins.authomatic.testing import AUTHOMATIC_PLONE_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest


class UpgradeStepIntegrationTest(unittest.TestCase):

    layer = AUTHOMATIC_PLONE_INTEGRATION_TESTING
    profile = "pas.plugins.authomatic:default"

    def setUp(self):
        self.portal = self.layer["portal"]
        self.setup = self.portal["portal_setup"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _match(self, item, source, dest):
        source, dest = tuple([source]), tuple([dest])
        return item["source"] == source and item["dest"] == dest

    def available_steps(self, src: str, dst: str) -> list:
        """Test available steps."""
        steps = listUpgradeSteps(self.setup, self.profile, src)
        steps = [s for s in steps if self._match(s[0], src, dst)]
        return steps

    @parameterized.expand(
        [
            ("1", "1000", 1),
        ]
    )
    def test_available(self, src, dst, expected):
        """Test upgrade step is available."""
        steps = self.available_steps(src, dst)
        self.assertEqual(len(steps), expected)
