# -*- coding: utf-8 -*-
from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings
from plone.app.registry.browser import controlpanel


class AuthomaticSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IPasPluginsAuthomaticSettings
    label = _(u"PAS Authomatic Plugin Settinss")
    description = _(u"")

    def updateFields(self):
        super(AuthomaticSettingsEditForm, self).updateFields()
        # self.fields['json_config'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super(AuthomaticSettingsEditForm, self).updateWidgets()


class AuthomaticSettingsEditFormSettingsControlPanel(
    controlpanel.ControlPanelFormWrapper
):
    form = AuthomaticSettingsEditForm
