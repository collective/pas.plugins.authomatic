from pas.plugins.authomatic import utils

import pytest


class TestIsRoot:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.portal = portal_class

    def test_portal_is_root(self):
        assert utils.is_root(self.portal) is True

    def test_non_root_object(self):
        # acl_users provides neither ISiteRoot nor INavigationRoot.
        assert utils.is_root(self.portal.acl_users) is False
