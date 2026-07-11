from __future__ import annotations

from authomatic.core import Authomatic
from collections.abc import Iterator
from pas.plugins.authomatic import _
from pas.plugins.authomatic import _types as t
from pas.plugins.authomatic import logger
from pas.plugins.authomatic import utils
from pas.plugins.authomatic.integration import ZopeRequestAdapter
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PluggableAuthService.PluggableAuthService import PluggableAuthService
from typing import cast
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from ZPublisher.HTTPRequest import WSGIRequest


@implementer(IPublishTraverse)
class AuthomaticView(BrowserView):
    template = ViewPageTemplateFile("authomatic.pt")
    _config: t.AuthomaticConfig

    zope_request_adapter_factory = ZopeRequestAdapter

    @property
    def zope_request_adapter(self) -> ZopeRequestAdapter:
        return self.zope_request_adapter_factory(self)

    def publishTraverse(self, request: WSGIRequest, name: str) -> AuthomaticView:
        if name and not hasattr(self, "provider"):
            self.provider = name
        return self

    @property
    def aclu(self) -> PluggableAuthService:
        return api.portal.get_tool("acl_users")

    @property
    def config(self) -> t.AuthomaticConfig:
        if not hasattr(self, "_config"):
            self._config = utils.authomatic_cfg()
        return self._config

    @property
    def _provider_names(self) -> list[str]:
        if not (cfgs := self.config):
            raise ValueError("Authomatic configuration has errors.")
        return list(cfgs.keys())

    def providers(self) -> Iterator[t.ProviderButton]:
        if not (cfgs := self.config):
            raise ValueError("Authomatic configuration has errors.")
        for identifier, cfg in cfgs.items():
            entry = cfg.get("display", {})
            cssclasses = entry.get("cssclasses", {})
            record: t.ProviderButton = {
                "identifier": identifier,
                "title": entry.get("title", identifier),
                "iconclasses": cssclasses.get("icon", "glypicon glyphicon-log-in"),
                "buttonclasses": cssclasses.get(
                    "button", "plone-btn plone-btn-default"
                ),
                "as_form": entry.get("as_form", False),
            }
            yield record

    def _add_identity(self, result: t.AuthResult, provider_name: str) -> None:
        # delegate to PAS plugin to add the identity
        utils.disable_csrf_protection(self.request)
        aclu = self.aclu
        aclu.authomatic.remember_identity(result)
        api.portal.show_message(
            _(
                "added_identity",
                default="Added identity provided by ${provider}",
                mapping={"provider": provider_name},
            ),
            self.request,
        )

    def _remember_identity(self, result: t.AuthResult, provider_name: str) -> None:
        utils.disable_csrf_protection(self.request)
        aclu = self.aclu
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
        if not (cfg := utils.authomatic_cfg()):
            return _("Authomatic is not configured")
        if not utils.is_root(self.context):
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
        secret = utils.authomatic_settings().secret
        auth = Authomatic(cfg, secret=secret)
        result = cast(
            "t.AuthResult | None", auth.login(self.zope_request_adapter, self.provider)
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
