# -*- coding: utf-8 -*-
from authomatic import Authomatic
from pas.plugins.authomatic.integration import ZopeRequestAdapter
from pas.plugins.authomatic.utils import authomatic_cfg
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
import logging

logger = logging.getLogger(__file__)


@implementer(IPublishTraverse)
class LoginView(BrowserView):

    template = ViewPageTemplateFile('login.pt')

    def publishTraverse(self, request, name):
        if name and not hasattr(self, 'provider'):
            self.provider = name
        return self

    def providers(self):
        cfgs = authomatic_cfg()
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
        if not hasattr(self, 'provider'):
            return self.template()
        cfg = authomatic_cfg()
        if cfg is None:

            return "Authomatic is not configured"
        if self.provider not in cfg:
            return "Provider not supported"
        auth = Authomatic(cfg, secret="very secret")
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

        # auth happend
        result.user.update()
        return result.user
