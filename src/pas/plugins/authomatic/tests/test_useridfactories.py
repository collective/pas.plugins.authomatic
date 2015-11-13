# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOBTree
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
from pas.plugins.authomatic.tests.mocks import MockResult
import unittest


class _MockPlugin(object):

    _useridentities_by_userid = OOBTree()


class TestUserIDFactories(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def test_normalizer(self):
        from pas.plugins.authomatic.useridfactories import BaseUserIDFactory
        bf = BaseUserIDFactory()

        mock_plugin = _MockPlugin()
        mock_result = MockResult()
        self.assertEqual('fo', bf.normalize(mock_plugin, mock_result, 'fo'))
        mock_plugin._useridentities_by_userid['fo'] = 1
        self.assertEqual('fo_2', bf.normalize(mock_plugin, mock_result, 'fo'))
