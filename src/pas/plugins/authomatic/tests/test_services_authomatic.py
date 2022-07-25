from pas.plugins.authomatic.testing import AUTHOMATIC_REST_API_TESTING
from plone.restapi.testing import RelativeSession
from urllib.parse import quote_plus

import unittest


class TestServiceAuthomaticGet(unittest.TestCase):
    layer = AUTHOMATIC_REST_API_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})

    def test_service_without_provider_id(self):
        response = self.api_session.get("@login-authomatic")
        self.assertEqual(404, response.status_code)
        data = response.json()
        error = data["error"]
        self.assertEqual(error["type"], "Provider not found")
        self.assertEqual(error["message"], "Provider was not informed.")

    def test_service_invalid_provider_id(self):
        response = self.api_session.get("@login-authomatic/unknown-provider")
        self.assertEqual(404, response.status_code)
        data = response.json()
        error = data["error"]
        self.assertEqual(error["type"], "Provider not found")
        self.assertEqual(
            error["message"], "Provider unknown-provider is not available."
        )

    def test_service_valid_provider_id(self):
        response = self.api_session.get("@login-authomatic/github")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIn("session", data)
        self.assertIn("next_url", data)
        self.assertIn(quote_plus("/plone/login-authomatic"), data["next_url"])

    def test_service_with_publicUrl(self):
        response = self.api_session.get(
            "@login-authomatic/github?publicUrl=https://plone.org"
        )
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIn("next_url", data)
        self.assertIn(
            quote_plus("https://plone.org/login-authomatic"), data["next_url"]
        )
