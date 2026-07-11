from pas.plugins.authomatic import utils
from zope.publisher.browser import TestRequest


class TestDisableCSRFProtection:
    def test_marks_request(self):
        from plone.protect.interfaces import IDisableCSRFProtection

        request = TestRequest()
        assert not IDisableCSRFProtection.providedBy(request)

        utils.disable_csrf_protection(request)
        assert IDisableCSRFProtection.providedBy(request)


class TestExtractAdapterParams:
    def test_removes_provider_and_public_url(self):
        request = TestRequest(
            form={
                "provider": "github",
                "publicUrl": "http://example.org",
                "code": "abc",
                "state": "xyz",
            }
        )
        assert utils.extract_adapter_params(request) == {"code": "abc", "state": "xyz"}

    def test_empty_form(self):
        assert utils.extract_adapter_params(TestRequest()) == {}

    def test_only_filtered_keys_returns_empty(self):
        request = TestRequest(form={"provider": "github", "publicUrl": "http://x"})
        assert utils.extract_adapter_params(request) == {}
