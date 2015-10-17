# -*- coding: utf-8 -*-
from authomatic.adapters import BaseAdapter
import logging

logger = logging.getLogger(__file__)


class ZopeRequestAdapter(BaseAdapter):
    """Adapter for Zope2 requests package."""

    def __init__(self, view):
        """
        :param request:
            Zope Request
        """
        self.view = view

    # =========================================================================
    # Request
    # =========================================================================

    @property
    def url(self):
        url = (
            self.view.context.absolute_url() +
            '/authomatic-login/' +
            self.view.provider
        )
        logger.info('url' + url)
        return url

    @property
    def params(self):
        return dict(self.view.request.form)

    @property
    def cookies(self):
        return self.view.request.cookies

    # =========================================================================
    # Response
    # =========================================================================

    def write(self, value):
        logger.info('write ' + value)
        self.view.request.response.write(value)

    def set_header(self, key, value):
        logger.info('set_header ' + key + '=' + value)
        self.view.request.response.setHeader(key, value)

    def set_status(self, status):
        code, message = status.split(' ')
        code = int(code)
        logger.info('set_status {0}'.format(code))
        self.view.request.response.setStatus(code)
