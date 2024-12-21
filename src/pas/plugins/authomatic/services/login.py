from pas.plugins.authomatic.utils import authomatic_cfg
from plone.restapi.services import Service


class Get(Service):
    """List available login options for the site."""

    @staticmethod
    def list_plugins() -> list[dict]:
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
            })
        return plugins

    def reply(self) -> dict[str, list[dict]]:
        """List login options available for the site.

        :returns: Login options information.
        """
        providers = self.list_plugins()
        return {"options": providers}
