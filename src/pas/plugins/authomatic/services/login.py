from pas.plugins.authomatic import _types as t
from pas.plugins.authomatic.utils.settings import authomatic_installed
from pas.plugins.authomatic.utils.settings import list_providers
from plone.base.interfaces import IPloneSiteRoot
from plone.dexterity.content import DexterityContent
from plone.restapi.interfaces import ILoginProviders
from zope.component import adapter
from zope.interface import implementer


@adapter(IPloneSiteRoot)
@implementer(ILoginProviders)
class AuthomaticLoginProviders:
    """Adapter returning all configured Authomatic login providers."""

    def __init__(self, context: DexterityContent) -> None:
        self.context = context

    def get_providers(self) -> list[t.LoginProvider]:
        """List all configured Authomatic plugins.

        The adapter is registered for the whole instance, so it is also asked
        on sites that never installed the add-on. Those sites offer no
        Authomatic providers.

        :returns: List of login options, empty when the add-on is not installed.
        """
        if not authomatic_installed():
            return []
        return list_providers(self.context.absolute_url())
