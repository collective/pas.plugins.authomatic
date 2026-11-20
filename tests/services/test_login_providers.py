from pas.plugins.authomatic import PACKAGE_NAME
from plone.restapi.interfaces import ILoginProviders
from zope.component import getAdapter
from zope.globalrequest import getRequest

import pytest


ADAPTER_NAME = "pas-plugins-authomatic-providers"


def clear_registry_request_cache() -> None:
    """Drop the registry values that plone.registry caches per request.

    The test layer reuses one request across tests, so a proxy cached by an
    earlier test would hide a missing record. A real request starts empty.
    """
    request = getRequest()
    if request is not None and getattr(request, "other", None) is not None:
        request.other.pop("_plone_registry_cache", None)


class TestLoginProvidersAdapter:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal
        self.adapter = getAdapter(portal, ILoginProviders, name=ADAPTER_NAME)

    def test_lists_providers_when_installed(self):
        providers = self.adapter.get_providers()
        assert [provider["id"] for provider in providers] == ["github"]

    def test_empty_when_addon_not_installed(self, installer):
        installer.uninstall_product(PACKAGE_NAME)
        clear_registry_request_cache()
        assert self.adapter.get_providers() == []
