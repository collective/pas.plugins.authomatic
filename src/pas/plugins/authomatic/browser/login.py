# -*- coding: utf-8 -*-
from authomatic import Authomatic
from pas.plugins.authomatic.utils import authomatic_cfg
from pas.plugins.authomatic.integration import ZopeRequestAdapter
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
import logging

logger = logging.getLogger(__file__)


@implementer(IPublishTraverse)
class LoginView(BrowserView):

    def publishTraverse(self, request, name):
        if not hasattr(self, 'provider'):
            self.provider = name
        return self

    def __call__(self):
        if not hasattr(self, 'provider'):
            return 'render tpl'
        cfg = authomatic_cfg()
        if cfg is None:
            return "Authomatic is not configured"
        # XXX validate if provider is valid/configured
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
        import ipdb; ipdb.set_trace()

