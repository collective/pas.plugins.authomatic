import pytest


@pytest.fixture()
def http_request(restapi):
    return restapi["request"]


@pytest.fixture()
def functional_portal(restapi):
    yield restapi["portal"]
