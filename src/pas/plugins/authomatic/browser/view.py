# -*- coding: utf-8 -*-
from authomatic import Authomatic
from pas.plugins.authomatic.integration import ZopeRequestAdapter
from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.utils import authomatic_cfg
from pas.plugins.authomatic.utils import authomatic_settings
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.protect.auto import safeWrite
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
import logging

logger = logging.getLogger(__file__)


@implementer(IPublishTraverse)
class AuthomaticView(BrowserView):

    template = ViewPageTemplateFile('authomatic.pt')

    def publishTraverse(self, request, name):
        if name and not hasattr(self, 'provider'):
            self.provider = name
        return self

    def providers(self):
        cfgs = authomatic_cfg()
        if not cfgs:
            raise ValueError("Authomatic configuration has errors.")
        for identifier, cfg in cfgs.items():
            entry = cfg.get('display', {})
            cssclasses = entry.get('cssclasses', {})
            record = {
                'identifier': identifier,
                'title': entry.get('title', identifier),
                'iconclasses': cssclasses.get(
                    'icon',
                    'glypicon glyphicon-log-in'
                ),
                'buttonclasses': cssclasses.get(
                    'button',
                    'plone-btn plone-btn-default'
                ),
                'as_form': entry.get('as_form', False),
            }
            yield record

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
                "{0}/authomatic-handler/{1}".format(
                    root.absolute_url(),
                    getattr(self, 'provider', '')
                )
            )
            return "redirecting"
        if not hasattr(self, 'provider'):
            return self.template()
        if self.provider not in cfg:
            return "Provider not supported"
        if not api.user.is_anonymous():
            # TODO: check if requested provider is already connected and
            #       fail if so
            # TODO: some sort of CSRF check might be needed, so that
            #       not an account got connected by CSRF. Research needed.
            pass
        auth = Authomatic(
            cfg,
            secret=authomatic_settings().secret.encode('utf8')
        )
        result = auth.login(
            ZopeRequestAdapter(self),
            self.provider
        )
        if not result:
            logger.info('return from view')
            # let authomatic do its work?
            return
        if result.error:
            return result.error.message
        display = cfg[self.provider].get('display', {})
        aclu = api.portal.get_tool('acl_users')
        if not api.user.is_anonymous():
            # now we delegate to PAS plugin to add the identity
            safeWrite(aclu.authomatic.remember_identity(result))
            api.portal.show_message(
                _(
                    'added_identity',
                    default='Added identity provided by ${provider}',
                    mapping={'provider': display.get('title', self.provider)}
                ),
                self.request
            )
            self.request.response.redirect(
                "{0}".format(self.context.absolute_url())
            )
        else:
            # now we delegate to PAS plugin to login
            safeWrite(aclu.authomatic.remember(result))
            display = cfg[self.provider].get('display', {})
            api.portal.show_message(
                _(
                    'logged_in_with',
                    'Logged in with ${provider}',
                    mapping={'provider': display.get('title', self.provider)}
                ),
                self.request
            )
            self.request.response.redirect(
                "{0}/login_success".format(self.context.absolute_url())
            )
        return "redirecting"
