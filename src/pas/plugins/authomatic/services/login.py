from pas.plugins.authomatic.utils import authomatic_cfg
from plone.base.interfaces import IPloneSiteRoot
from plone.restapi.interfaces import ILoginProviders
from zope.component import adapter
from zope.interface import implementer


@adapter(IPloneSiteRoot)
@implementer(ILoginProviders)
class AuthomaticLoginProviders:
    def __init__(self, context):
        self.context = context

    def get_providers(self) -> list[dict]:
        """List all configured Authomatic plugins.

        :returns: List of login options.
        """
        try:
            providers = authomatic_cfg()
        except KeyError:
            # Authomatic is not configured
            providers = {}
        plugins = []
        for provider_id, provider in providers.items():
            entry = provider.get("display", {})
            title = entry.get("title", provider_id)

            plugins.append({
                "id": provider_id,
                "plugin": "authomatic",
                "title": title,
                "url": f"{self.context.absolute_url()}/@login-oidc/{provider_id}",
            })
        return plugins
