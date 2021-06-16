from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from plone.app.registry.browser import controlpanel


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
