from pas.plugins.authomatic import _types as t
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

        :returns: List of login options.
        """
        return list_providers(self.context.absolute_url())
