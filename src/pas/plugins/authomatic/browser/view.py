from __future__ import annotations

from authomatic.core import Authomatic
from collections.abc import Iterator
from pas.plugins.authomatic import logger
from pas.plugins.authomatic._types import AuthResult
from pas.plugins.authomatic._types import ProviderButton
from pas.plugins.authomatic.integration import ZopeRequestAdapter
from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.utils import authomatic_cfg
from pas.plugins.authomatic.utils import authomatic_settings
from plone import api
from plone.base.interfaces.siteroot import INavigationRoot
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from typing import cast
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from ZPublisher.HTTPRequest import WSGIRequest


def is_root(obj) -> bool:
    """Check if current context is Navigation root or a Portal."""
    return ISiteRoot.providedBy(obj) or INavigationRoot.providedBy(obj)


@implementer(IPublishTraverse)
class AuthomaticView(BrowserView):
    template = ViewPageTemplateFile("authomatic.pt")

    zope_request_adapter_factory = ZopeRequestAdapter

    @property
    def zope_request_adapter(self) -> ZopeRequestAdapter:
        return self.zope_request_adapter_factory(self)

    def publishTraverse(self, request: WSGIRequest, name: str) -> AuthomaticView:
        if name and not hasattr(self, "provider"):
            self.provider = name
        return self

    @property
    def _provider_names(self) -> list[str]:
        if not (cfgs := authomatic_cfg()):
            raise ValueError("Authomatic configuration has errors.")
        return list(cfgs.keys())

    def providers(self) -> Iterator[ProviderButton]:
        cfgs = authomatic_cfg()
        if not cfgs:
            raise ValueError("Authomatic configuration has errors.")
        for identifier, cfg in cfgs.items():
            entry = cfg.get("display", {})
            cssclasses = entry.get("cssclasses", {})
            record: ProviderButton = {
                "identifier": identifier,
                "title": entry.get("title", identifier),
                "iconclasses": cssclasses.get("icon", "glypicon glyphicon-log-in"),
                "buttonclasses": cssclasses.get(
                    "button", "plone-btn plone-btn-default"
                ),
                "as_form": entry.get("as_form", False),
            }
            yield record

    def _add_identity(self, result: AuthResult, provider_name: str) -> None:
        # delegate to PAS plugin to add the identity
        alsoProvides(self.request, IDisableCSRFProtection)
        aclu = api.portal.get_tool("acl_users")
        aclu.authomatic.remember_identity(result)
        api.portal.show_message(
            _(
                "added_identity",
                default="Added identity provided by ${provider}",
                mapping={"provider": provider_name},
            ),
            self.request,
        )

    def _remember_identity(self, result: AuthResult, provider_name: str) -> None:
        alsoProvides(self.request, IDisableCSRFProtection)
        aclu = api.portal.get_tool("acl_users")
        aclu.authomatic.remember(result)
        api.portal.show_message(
            _(
                "logged_in_with",
                "Logged in with ${provider}",
                mapping={"provider": provider_name},
            ),
            self.request,
        )

    def _handle_error(self, error) -> str:
        try:
            return error.message
        except AttributeError:
            return str(error)

    def _redirect(self) -> str:
        next_url = self.request.cookies.get("next_url", "")
        self.request.response.expireCookie("next_url")
        self.request.response.redirect(self.context.absolute_url() + next_url)
        return _("redirecting")

    @property
    def is_anon(self) -> bool:
        return api.user.is_anonymous()

    def __call__(self) -> str | None:
        provider = getattr(self, "provider", "")
        if not (cfg := authomatic_cfg()):
            return _("Authomatic is not configured")
        if not is_root(self.context):
            # callback url is expected on either navigationroot or site root
            # so bevor going on redirect
            root = api.portal.get_navigation_root(self.context)
            root_url = root.absolute_url()
            self.request.response.redirect(f"{root_url}/authomatic-handler/{provider}")
            return _("redirecting")
        if not provider:
            return self.template()
        elif provider not in cfg:
            return _("Provider not supported")
        if not self.is_anon:
            if provider in self._provider_names:
                logger.warning(
                    f"Provider {provider} is already connected to current user"
                )
                return self._redirect()
            # TODO: some sort of CSRF check might be needed, so that
            #       not an account got connected by CSRF. Research needed.
            pass
        secret = authomatic_settings().secret
        auth = Authomatic(cfg, secret=secret)
        result = cast(
            "AuthResult | None", auth.login(self.zope_request_adapter, self.provider)
        )
        if not result:
            logger.info("return from view")
            # let authomatic do its work
            return None
        elif error := result.error:
            return self._handle_error(error)
        display = cfg[self.provider].get("display", {})
        provider_name = display.get("title", self.provider)
        if not self.is_anon:
            # now we delegate to PAS plugin to add the identity
            self._add_identity(result, provider_name)
        else:
            # now we delegate to PAS plugin in order to login
            self._remember_identity(result, provider_name)

        return self._redirect()
