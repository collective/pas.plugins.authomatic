from pas.plugins.authomatic.testing import AUTHOMATIC_REST_API_TESTING
from plone.restapi.testing import RelativeSession

import unittest


class TestServiceLogin(unittest.TestCase):
    layer = AUTHOMATIC_REST_API_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})

    def test_login_options(self):
        response = self.api_session.get("@login")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIs(type(data), dict)
        self.assertIn("options", data)
        self.assertEqual(len(data["options"]), 1)
        option = data["options"][0]
        self.assertEqual(option["id"], "github")
        self.assertEqual(option["plugin"], "authomatic")
        self.assertEqual(option["title"], "Github")
