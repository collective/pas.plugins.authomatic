# -*- coding: utf-8 -*-
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
from pas.plugins.authomatic.tests.mocks import MockResult
import unittest


class TestUserIdentities(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def test_identity_init(self):
        input_name = 'mockprovider'
        mock_result = MockResult(
            provider=MockResult(name=input_name),
            user=MockResult(),
        )
        from pas.plugins.authomatic.useridentities import UserIdentity
        ui = UserIdentity(mock_result)
        self.assertEqual(ui['provider_name'], input_name)

    def test_identities_init(self):
        input_userid = 'mockuserid'
        from pas.plugins.authomatic.useridentities import UserIdentities
        uis = UserIdentities(input_userid)
        self.assertEqual(uis.userid, input_userid)

    # def test_existing_user_attributes(self):
    #     user = self._make_one()
    #     propmap = self._make_propmap()
    #     result = self.plugin._make_sheet(user, propmap)
    #     self.assertIsInstance(result, UserPropertySheet)
    #     self.assertEqual(
    #         result.getProperty('home_page'),
    #         u'http://peterhudec.github.io/authomatic/'
    #     )
    #     self.assertEqual(result.getProperty('fullname'), u'Andrew Pipkin')
    #     self.assertEqual(
    #         result.getProperty('email'),
    #         u'andrewpipkin@foobar.com'
    #     )

    # def test_provider_specific_user_attributes(self):
    #     user = self._make_one()
    #     propmap = self._make_propmap()
    #     propmap['data'] = {'domain': 'domain'}

    #     result = self.plugin._make_sheet(user, propmap)
    #     self.assertIsInstance(result, UserPropertySheet)
    #     self.assertEqual(
    #         result.getProperty('home_page'),
    #         u'http://peterhudec.github.io/authomatic/'
    #     )
    #     self.assertEqual(result.getProperty('fullname'), u'Andrew Pipkin')
    #     self.assertEqual(
    #         result.getProperty('email'),
    #         u'andrewpipkin@foobar.com'
    #     )
    #     self.assertEqual(result.getProperty('domain'), u'foobar.com')
