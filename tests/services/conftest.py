from plone.restapi.testing import RelativeSession
from zope.component.hooks import setSite

import pytest


@pytest.fixture()
def http_request(restapi):
    return restapi["request"]


@pytest.fixture()
def portal(restapi):
    portal = restapi["portal"]
    setSite(portal)
    yield portal


@pytest.fixture()
def request_api_factory(portal):
    def factory():
        url = portal.absolute_url()
        api_session = RelativeSession(f"{url}/++api++")
        return api_session

    return factory


@pytest.fixture()
def api_anon_request(request_api_factory):
    return request_api_factory()
