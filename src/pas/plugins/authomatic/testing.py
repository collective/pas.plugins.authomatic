from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.protect import auto
from plone.testing import Layer
from plone.testing.zope import installProduct
from plone.testing.zope import INTEGRATION_TESTING
from plone.testing.zope import WSGI_SERVER_FIXTURE
from Products.CMFCore.interfaces import ISiteRoot
from Products.PlonePAS.setuphandlers import migrate_root_uf
from zope.component import provideUtility

import pas.plugins.authomatic


ORIGINAL_CSRF_DISABLED = auto.CSRF_DISABLED


class PasPluginsAuthomaticZopeLayer(Layer):

    defaultBases = (INTEGRATION_TESTING,)

    # Products that will be installed, plus options
    products = (
        (
            "Products.GenericSetup",
            {"loadZCML": True},
        ),
        (
            "Products.CMFCore",
            {"loadZCML": True},
        ),
        (
            "Products.PluggableAuthService",
            {"loadZCML": True},
        ),
        (
            "Products.PluginRegistry",
            {"loadZCML": True},
        ),
        (
            "Products.PlonePAS",
            {"loadZCML": True},
        ),
    )

    def setUp(self):
        self.setUpZCML()

    def testSetUp(self):
        self.setUpProducts()
        provideUtility(self["app"], provides=ISiteRoot)
        migrate_root_uf(self["app"])

    def setUpZCML(self):
        """Stack a new global registry and load ZCML configuration of Plone
        and the core set of add-on products into it.
        """

        # Load dependent products's ZCML
        from zope.configuration import xmlconfig
        from zope.dottedname.resolve import resolve

        def loadAll(filename):
            for p, config in self.products:
                if not config["loadZCML"]:
                    continue
                try:
                    package = resolve(p)
                except ImportError:
                    continue
                try:
                    xmlconfig.file(
                        filename, package, context=self["configurationContext"]
                    )
                except OSError:
                    pass

        loadAll("meta.zcml")
        loadAll("configure.zcml")
        loadAll("overrides.zcml")

    def setUpProducts(self):
        """Install all old-style products listed in the the ``products`` tuple
        of this class.
        """
        for prd, config in self.products:
            installProduct(self["app"], prd)


AUTHOMATIC_ZOPE_FIXTURE = PasPluginsAuthomaticZopeLayer()


class PasPluginsAuthomaticPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        auto.CSRF_DISABLED = True
        self.loadZCML(package=pas.plugins.authomatic)
        installProduct(app, "pas.plugins.authomatic")

    def tearDownZope(self, app):
        auto.CSRF_DISABLED = ORIGINAL_CSRF_DISABLED

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.restapi:default")
        applyProfile(portal, "pas.plugins.authomatic:default")


AUTHOMATIC_PLONE_FIXTURE = PasPluginsAuthomaticPloneLayer()


AUTHOMATIC_PLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(AUTHOMATIC_PLONE_FIXTURE,),
    name="PasPluginsAuthomaticPloneLayer:IntegrationTesting",
)


AUTHOMATIC_PLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(AUTHOMATIC_PLONE_FIXTURE,),
    name="PasPluginsAuthomaticPloneLayer:FunctionalTesting",
)


AUTHOMATIC_REST_API_TESTING = FunctionalTesting(
    bases=(AUTHOMATIC_PLONE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="PasPluginsAuthomaticPloneLayer:RestAPITesting",
)


AUTHOMATIC_PLONE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        AUTHOMATIC_PLONE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="PasPluginsAuthomaticPloneLayer:AcceptanceTesting",
)
