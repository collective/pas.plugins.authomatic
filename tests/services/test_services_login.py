import pytest


class TestServiceLogin:
    @pytest.fixture(autouse=True)
    def _setup(self, api_anon_request):
        self.api_session = api_anon_request

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
