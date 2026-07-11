from plone.protect.interfaces import IDisableCSRFProtection
from typing import Any
from zope.interface import alsoProvides
from ZPublisher.HTTPRequest import WSGIRequest


def disable_csrf_protection(request: WSGIRequest) -> None:
    """Disable CSRF protection for the given request."""
    alsoProvides(request, IDisableCSRFProtection)


def extract_adapter_params(request: WSGIRequest) -> dict[str, Any]:
    """Extract adapter parameters from the request.

    :param request: The WSGI request object.
    :returns: Dictionary with adapter parameters.
    """
    params = dict(request.form)
    to_remove = ["provider", "publicUrl"]
    return {k: v for k, v in params.items() if k not in to_remove}
