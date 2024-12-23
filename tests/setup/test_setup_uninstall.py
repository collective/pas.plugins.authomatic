from pas.plugins.authomatic import PACKAGE_NAME

import pytest


class TestSetupUninstall:
    @pytest.fixture(autouse=True)
    def uninstalled(self, installer):
        installer.uninstall_product(PACKAGE_NAME)

    def test_addon_uninstalled(self, installer):
        """Test if kitconcept_intranet is uninstalled."""
        assert installer.is_product_installed(PACKAGE_NAME) is False

    def test_browserlayer_not_registered(self, browser_layers):
        """Test that IDefaultBrowserLayer is not registered."""
        from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticLayer

        assert IPasPluginsAuthomaticLayer not in browser_layers
