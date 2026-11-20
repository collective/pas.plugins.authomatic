from pas.plugins.authomatic import PACKAGE_NAME
from plone.base.utils import get_installer

import pytest
import transaction


class TestServiceLogin:
    @pytest.fixture(autouse=True)
    def _setup(self, anon_request):
        self.api_session = anon_request

    def test_get_login_endpoint(self):
        response = self.api_session.get("/@login")
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["id", "github"],
            ["plugin", "authomatic"],
            ["title", "Github"],
        ],
    )
    def test_get_login_options(self, key, expected):
        response = self.api_session.get("/@login")
        data = response.json()
        options = data.get("options")
        assert len(options) == 1
        option = data["options"][0]
        assert option[key] == expected


class TestServiceLoginWithoutAddon:
    @pytest.fixture(autouse=True)
    def _setup(self, restapi, anon_request):
        get_installer(restapi["portal"]).uninstall_product(PACKAGE_NAME)
        # The WSGI server handles requests on its own connection, so it only
        # sees the uninstall once it is committed.
        transaction.commit()
        self.api_session = anon_request

    def test_get_login_endpoint_answers_200(self):
        response = self.api_session.get("/@login")
        assert response.status_code == 200
        assert response.json().get("options") == []
