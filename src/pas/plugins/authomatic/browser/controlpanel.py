# -*- coding: utf-8 -*-
from pas.plugins.authomatic.interfaces import _
from pas.plugins.authomatic.interfaces import IPasPluginsAuthomaticSettings  # noqa
from plone.app.registry.browser import controlpanel
from z3c.form.browser.textlines import TextLinesFieldWidget


class MemberpropertiestogroupSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IPasPluginsAuthomaticSettings
    label = _(u"Member Properties To Group Settings")
    description = _(u"")

    def updateFields(self):
        super(MemberpropertiestogroupSettingsEditForm, self).updateFields()
        self.fields['valid_groups'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super(MemberpropertiestogroupSettingsEditForm, self).updateWidgets()


class MemberpropertiestogroupSettingsEditFormSettingsControlPanel(controlpanel.ControlPanelFormWrapper):  # noqa
    form = MemberpropertiestogroupSettingsEditForm
