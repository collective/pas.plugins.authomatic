from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser
from zope.component.hooks import setSite

import pytest


@pytest.fixture()
def http_request(functional):
    return functional["request"]


@pytest.fixture()
def portal(functional):
    portal = functional["portal"]
    setSite(portal)
    yield portal


@pytest.fixture
def browser(app):
    browser = Browser(app)
    browser.handleErrors = False


@pytest.fixture()
def browser_factory(app):
    def factory(handle_errors=True):
        browser = Browser(app)
        browser.handleErrors = handle_errors
        return browser

    return factory


@pytest.fixture()
def browser_manager(browser_factory):
    browser = browser_factory()
    browser.addHeader(
        "Authorization",
        f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
    )
    return browser


class TestControlPanelFunctional:
    @pytest.fixture(autouse=True)
    def _initialize(self, http_request, portal, browser_manager):
        self.portal = portal
        self.portal_url = portal.absolute_url()
        self.request = http_request
        self.browser = browser_manager

    def test_empty_form(self):
        self.browser.open(f"{self.portal_url}/authomatic-controlpanel")
        assert " Settings" in self.browser.contents
