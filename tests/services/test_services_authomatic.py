from urllib.parse import quote_plus

import pytest


class TestServiceAuthomaticGet:
    @pytest.fixture(autouse=True)
    def _setup(self, api_anon_request):
        self.api_session = api_anon_request

    @pytest.mark.parametrize(
        "url,error_type,error_message",
        [
            ["/@login-authomatic", "Provider not found", "Provider was not informed."],
            [
                "/@login-authomatic/unknown-provider",
                "Provider not found",
                "Provider unknown-provider is not available.",
            ],
            [
                "/@login-authomatic/unknown-provider",
                "Provider not found",
                "Provider unknown-provider is not available.",
            ],
        ],
    )
    def test_service_without_provider_id(self, url, error_type, error_message):
        response = self.api_session.get(url)
        assert response.status_code == 404
        data = response.json()
        error = data["error"]
        assert error["type"] == error_type
        assert error["message"] == error_message

    def test_service_valid_provider_id(self):
        response = self.api_session.get("/@login-authomatic/github")
        assert response.status_code == 200
        data = response.json()
        assert "session" in data
        assert "next_url" in data
        assert quote_plus("/plone/login-authomatic") in data["next_url"]

    def test_service_with_publicUrl(self):
        response = self.api_session.get(
            "/@login-authomatic/github?publicUrl=https://plone.org"
        )
        assert response.status_code == 200
        data = response.json()
        assert "session" in data
        assert "next_url" in data
        assert quote_plus("https://plone.org/login-authomatic") in data["next_url"]
