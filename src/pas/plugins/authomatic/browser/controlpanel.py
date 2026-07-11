from pas.plugins.authomatic import _
from pas.plugins.authomatic import interfaces as ifaces
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


class AuthomaticSettingsEditForm(controlpanel.RegistryEditForm):
    label = _("PAS Authomatic Plugin Settings")
    description = ""

    @property
    def schema(self):
        return ifaces.IPasPluginsAuthomaticSettings

    def updateFields(self) -> None:
        super().updateFields()
        # self.fields['json_config'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self) -> None:
        super().updateWidgets()


class AuthomaticSettingsEditFormSettingsControlPanel(
    controlpanel.ControlPanelFormWrapper
):
    form = AuthomaticSettingsEditForm


@adapter(Interface, ifaces.IPasPluginsAuthomaticLayer)
class AuthomaticSettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = ifaces.IPasPluginsAuthomaticSettings
    configlet_id = "authomatic"
    configlet_category_id = "plone-users"
    title = _("Authomatic settings")
    group = ""
    schema_prefix = "pas.plugins.authomatic.interfaces.IPasPluginsAuthomaticSettings"
