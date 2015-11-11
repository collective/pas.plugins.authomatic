# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOBTree
from pas.plugins.authomatic.testing import PAS_PLUGINS_Authomatic_ZOPE_FIXTURE
import unittest


class MockPlugin(object):

    _uid_to_userdata = OOBTree()


class TestUserIDFactories(unittest.TestCase):

    layer = PAS_PLUGINS_Authomatic_ZOPE_FIXTURE

    def test_normalizer(self):
        from pas.plugins.authomatic.useridfactories import BaseUserIDFactory
        bf = BaseUserIDFactory(MockPlugin())

        self.assertEqual('foo', bf.normalize('foo'))
        bf._uid_to_userdata['foo'] = 1
        self.assertEqual('foo_2', bf.normalize('foo'))
