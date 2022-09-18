from pas.plugins.authomatic.testing import AUTHOMATIC_ZOPE_FIXTURE
from pas.plugins.authomatic.tests.mocks import make_user
from pas.plugins.authomatic.tests.mocks import MockResult
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from unittest import mock

import unittest


class TestUserIdentity(unittest.TestCase):

    layer = AUTHOMATIC_ZOPE_FIXTURE

    def test_init(self):
        input_name = "mockprovider"
        mock_result = MockResult(
            provider=MockResult(name=input_name),
            user=MockResult(),
        )
        from pas.plugins.authomatic.useridentities import UserIdentity

        ui = UserIdentity(mock_result)
        self.assertEqual(ui["provider_name"], input_name)


class TestUserIdentities(unittest.TestCase):

    layer = AUTHOMATIC_ZOPE_FIXTURE

    def _make_authomatic_user(self, provider_name="MockPlone", data=None):
        from authomatic.core import User

        provider = MockResult(name=provider_name)
        if not data:
            data = {
                "displayName": "Andrew Pipkin",
                "domain": "foobar.com",
                "emails": [{"type": "account", "value": "andrewpipkin@foobar.com"}],
                "etag": '"xxxxxxxxxxxx/xxxxxxxxxxxx"',
                "id": "123456789",
                "image": {
                    "isDefault": False,
                    "url": "https://lh3.googleusercontent.com/photo.jpg",
                },
                "isPlusUser": False,
                "kind": "plus#person",
                "language": "en_GB",
                "name": {"familyName": "Pipkin", "givenName": "Andrew"},
                "objectType": "person",
                "verified": False,
            }
        user = User(provider)
        user.data = data
        user.id = "123456789"
        user.username = "andrewpipkin"
        user.name = "Andrew Pipkin"
        user.first_name = "Andrew"
        user.last_name = "Pipkin"
        user.nickname = "Andy"
        user.link = "http://peterhudec.github.io/authomatic/"
        user.email = "andrewpipkin@foobar.com"
        user.picture = "https://lh3.googleusercontent.com/photo.jpg?sz=50"
        user.location = "Innsbruck"

        # from authomatic.core import Credentials
        # user.credentials = Credentials()

        return user

    def _make_cfg(self, provider="provider"):
        propmap = {
            "email": "email",
            "link": "home_page",
            "location": "location",
            "name": "fullname",
        }
        return {
            provider: {
                "propertymap": propmap,
            }
        }

    def test_identities_init(self):
        input_userid = "mockuserid"
        from pas.plugins.authomatic.useridentities import UserIdentities

        uis = UserIdentities(input_userid)
        self.assertEqual(uis.userid, input_userid)

    def test_sheet_existing_user_attributes(self):
        # mock a user
        PNAME = "mockhub"
        authomatic_result = MockResult(
            user=self._make_authomatic_user(provider_name=PNAME),
            provider=MockResult(name=PNAME),
        )
        uis = make_user("mustermann")
        uis.handle_result(authomatic_result)

        # mock cfg
        with mock.patch("pas.plugins.authomatic.useridentities.authomatic_cfg") as cfg:
            cfg.return_value = self._make_cfg(PNAME)
            sheet = uis.propertysheet
        self.assertIsInstance(sheet, UserPropertySheet)
        self.assertEqual(
            sheet.getProperty("home_page"), "http://peterhudec.github.io/authomatic/"
        )
        self.assertEqual(sheet.getProperty("fullname"), "Andrew Pipkin")
        self.assertEqual(sheet.getProperty("email"), "andrewpipkin@foobar.com")

    def test_provider_specific_user_attributes(self):
        # mock a user
        PNAME = "mockhub"
        authomatic_result = MockResult(
            user=self._make_authomatic_user(provider_name=PNAME),
            provider=MockResult(name=PNAME),
        )
        uis = make_user("mustermann")
        uis.handle_result(authomatic_result)

        # mock cfg
        with mock.patch("pas.plugins.authomatic.useridentities.authomatic_cfg") as acfg:
            cfg = self._make_cfg(PNAME)
            cfg[PNAME]["propertymap"]["domain"] = "customdomain"
            acfg.return_value = cfg
            sheet = uis.propertysheet
        self.assertIsInstance(sheet, UserPropertySheet)
        self.assertEqual(
            sheet.getProperty("home_page"), "http://peterhudec.github.io/authomatic/"
        )
        self.assertEqual(sheet.getProperty("fullname"), "Andrew Pipkin")
        self.assertEqual(sheet.getProperty("email"), "andrewpipkin@foobar.com")
        self.assertEqual(sheet.getProperty("customdomain"), "foobar.com")

    def test_credentials(self):
        pass
