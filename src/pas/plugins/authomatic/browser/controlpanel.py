from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticLayer
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from plone.app.registry.browser import controlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


class AuthomaticSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IPasPluginsAuthomaticSettings
    label = _("PAS Authomatic Plugin Settings")
    description = ""

    def updateFields(self):
        super().updateFields()
        # self.fields['json_config'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super().updateWidgets()


class AuthomaticSettingsEditFormSettingsControlPanel(
    controlpanel.ControlPanelFormWrapper
):
    form = AuthomaticSettingsEditForm


@adapter(Interface, IPasPluginsAuthomaticLayer)
class AuthomaticSettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IPasPluginsAuthomaticSettings
    configlet_id = "authomatic"
    configlet_category_id = "Products"
    title = _("Authomatic settings")
    group = ""
    schema_prefix = "pas.plugins.authomatic.interfaces.IPasPluginsAuthomaticSettings"
