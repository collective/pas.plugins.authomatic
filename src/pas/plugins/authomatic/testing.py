# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.protect import auto
from plone.testing import Layer
from plone.testing import z2
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import provideUtility
from Products.PlonePAS.setuphandlers import migrate_root_uf

import pas.plugins.authomatic


ORIGINAL_CSRF_DISABLED = auto.CSRF_DISABLED


class PasPluginsAuthomaticZopeLayer(Layer):

    defaultBases = (
        z2.INTEGRATION_TESTING,
    )

    # Products that will be installed, plus options
    products = (
        ('Products.GenericSetup', {'loadZCML': True}, ),
        ('Products.CMFCore', {'loadZCML': True}, ),
        ('Products.PluggableAuthService', {'loadZCML': True}, ),
        ('Products.PluginRegistry', {'loadZCML': True}, ),
        ('Products.PlonePAS', {'loadZCML': True}, ),
    )

    def setUp(self):
        self.setUpZCML()

    def testSetUp(self):
        self.setUpProducts()
        provideUtility(self['app'], provides=ISiteRoot)
        migrate_root_uf(self['app'])

    def setUpZCML(self):
        """Stack a new global registry and load ZCML configuration of Plone
        and the core set of add-on products into it.
        """

        # Load dependent products's ZCML
        from zope.configuration import xmlconfig
        from zope.dottedname.resolve import resolve

        def loadAll(filename):
            for p, config in self.products:
                if not config['loadZCML']:
                    continue
                try:
                    package = resolve(p)
                except ImportError:
                    continue
                try:
                    xmlconfig.file(
                        filename,
                        package,
                        context=self['configurationContext']
                    )
                except IOError:
                    pass

        loadAll('meta.zcml')
        loadAll('configure.zcml')
        loadAll('overrides.zcml')

    def setUpProducts(self):
        """Install all old-style products listed in the the ``products`` tuple
        of this class.
        """
        for prd, config in self.products:
            z2.installProduct(self['app'], prd)


PAS_PLUGINS_Authomatic_ZOPE_FIXTURE = PasPluginsAuthomaticZopeLayer()


class PasPluginsAuthomaticPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        auto.CSRF_DISABLED = True
        self.loadZCML(package=pas.plugins.authomatic)
        z2.installProduct(app, 'pas.plugins.authomatic')

    def tearDownZope(self, app):
        auto.CSRF_DISABLED = ORIGINAL_CSRF_DISABLED

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'pas.plugins.authomatic:default')


PAS_PLUGINS_Authomatic_PLONE_FIXTURE = PasPluginsAuthomaticPloneLayer()


PAS_PLUGINS_Authomatic_PLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PAS_PLUGINS_Authomatic_PLONE_FIXTURE,),
    name='PasPluginsAuthomaticPloneLayer:IntegrationTesting'
)


PAS_PLUGINS_Authomatic_PLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PAS_PLUGINS_Authomatic_PLONE_FIXTURE,),
    name='PasPluginsAuthomaticPloneLayer:FunctionalTesting'
)


PAS_PLUGINS_Authomatic_PLONE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PAS_PLUGINS_Authomatic_PLONE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PasPluginsAuthomaticPloneLayer:AcceptanceTesting'
)
