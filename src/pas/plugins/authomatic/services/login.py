from pas.plugins.authomatic.utils import authomatic_cfg
from plone.base.interfaces import IPloneSiteRoot
from plone.restapi.interfaces import IExternalLoginProviders
from zope.component import adapter
from zope.interface import implementer


@adapter(IPloneSiteRoot)
@implementer(IExternalLoginProviders)
class AuthomaticLoginProviders:
    def __init__(self, context):
        self.context = context

    def get_providers(self):
        options = []
        providers = authomatic_cfg()
        for provider_id, provider in providers.items():
            entry = provider.get("display", {})
            title = entry.get("title", provider_id)
            options.append(
                dict(
                    id=provider_id,
                    plugin="authomatic",
                    title=title,
                    url=self.context.absolute_url() + '/@login-authomatic/' + provider_id
                )
            )

        return {"options": options}

