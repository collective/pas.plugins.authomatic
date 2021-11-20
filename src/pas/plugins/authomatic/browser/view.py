from authomatic import Authomatic
from pas.plugins.authomatic.integration import ZopeRequestAdapter
from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.utils import authomatic_cfg
from pas.plugins.authomatic.utils import authomatic_settings
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import logging


logger = logging.getLogger(__file__)


@implementer(IPublishTraverse)
class AuthomaticView(BrowserView):

    template = ViewPageTemplateFile("authomatic.pt")

    def publishTraverse(self, request, name):
        if name and not hasattr(self, "provider"):
            self.provider = name
        return self

    @property
    def _provider_names(self):
        cfgs = authomatic_cfg()
        if not cfgs:
            raise ValueError("Authomatic configuration has errors.")
        return list(cfgs.keys())

    def providers(self):
        cfgs = authomatic_cfg()
        if not cfgs:
            raise ValueError("Authomatic configuration has errors.")
        for identifier, cfg in cfgs.items():
            entry = cfg.get("display", {})
            cssclasses = entry.get("cssclasses", {})
            record = {
                "identifier": identifier,
                "title": entry.get("title", identifier),
                "iconclasses": cssclasses.get("icon", "glypicon glyphicon-log-in"),
                "buttonclasses": cssclasses.get(
                    "button", "plone-btn plone-btn-default"
                ),
                "as_form": entry.get("as_form", False),
            }
            yield record

    def _add_identity(self, result, provider_name):
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

    def _remember_identity(self, result, provider_name):
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

    def __call__(self):
        cfg = authomatic_cfg()
        if cfg is None:
            return "Authomatic is not configured"
        if not (
            ISiteRoot.providedBy(self.context)
            or INavigationRoot.providedBy(self.context)
        ):
            # callback url is expected on either navigationroot or site root
            # so bevor going on redirect
            root = api.portal.get_navigation_root(self.context)
            self.request.response.redirect(
                "{}/authomatic-handler/{}".format(
                    root.absolute_url(), getattr(self, "provider", "")
                )
            )
            return "redirecting"
        if not getattr(self, "provider", None):
            return self.template()
        if self.provider not in cfg:
            return "Provider not supported"
        if not self.is_anon:
            if self.provider in self._provider_names:
                raise ValueError(
                    "Provider {} is already connected to current "
                    "user.".format(self.provider)
                )
            # TODO: some sort of CSRF check might be needed, so that
            #       not an account got connected by CSRF. Research needed.
            pass
        secret = authomatic_settings().secret
        auth = Authomatic(cfg, secret=secret)
        result = auth.login(ZopeRequestAdapter(self), self.provider)
        if not result:
            logger.info("return from view")
            # let authomatic do its work
            return
        if result.error:
            return result.error.message
        display = cfg[self.provider].get("display", {})
        provider_name = display.get("title", self.provider)
        if not self.is_anon:
            # now we delegate to PAS plugin to add the identity
            self._add_identity(result, provider_name)
        else:
            # now we delegate to PAS plugin in order to login
            self._remember_identity(result, provider_name)

        came_from = self.request.cookies.get('came_from', '/ads')
        self.request.response.redirect(
            self.context.absolute_url() + came_from
        )
        return "redirecting"

    @property
    def is_anon(self):
        return api.user.is_anonymous()
