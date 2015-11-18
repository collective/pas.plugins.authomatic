import logging

from Products.CMFPlone.utils import getFSVersionTuple
logger = logging.getLogger('pas.plugins.authomatic')


def install(portal, reinstall=False):
    setup_tool = portal.portal_setup
    version = getFSVersionTuple()[0]

    if version < 5:
        setup_tool.runAllImportStepsFromProfile(
            'profile-pas.plugins.authomatic:plone4')
    else:
        setup_tool.runAllImportStepsFromProfile(
            'profile-pas.plugins.authomatic:plone5')
    logger.info("Installed")


def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile(
            'profile-pas.plugins.authomatic:uninstall')
        logger.info("Uninstalled")
