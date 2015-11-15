# -*- coding: utf-8 -*-
from authomatic import Authomatic
from pas.plugins.authomatic.integration import ZopeRequestAdapter
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
        if not api.user.is_anonymous():
            api.portal.show_message(
                'You are already logged in!',
                self.request,
                'error'
            )
            self.request.response.redirect(self.context.absolute_url())
            return "redirecting"

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
        cfg = authomatic_cfg()
        if cfg is None:
            return "Authomatic is not configured"
        if self.provider not in cfg:
            return "Provider not supported"
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

        # now we delegate to the PAS plugin to store the information fetched
        aclu = api.portal.get_tool('acl_users')
        safeWrite(aclu.authomatic.remember(result))
        display = cfg[self.provider].get('display', {})
        api.portal.show_message(
            'Logged in with {0}'.format(display.get('title', self.provider)),
            self.request
        )
        self.request.response.redirect(
            "{0}/login_success".format(self.context.absolute_url())
        )
        return "redirecting"
