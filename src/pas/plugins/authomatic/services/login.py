from pas.plugins.authomatic.utils import authomatic_cfg
from plone.restapi.services import Service
from typing import Dict
from typing import List


class Get(Service):
    """List available login options for the site."""

    @staticmethod
    def list_plugins() -> List[Dict]:
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
            plugins.append(
                dict(
                    id=provider_id,
                    plugin="authomatic",
                    title=title,
                )
            )
        return plugins

    def reply(self) -> Dict[str, List[Dict]]:
        """List login options available for the site.

        :returns: Login options information.
        """
        providers = self.list_plugins()
        return {"options": providers}
