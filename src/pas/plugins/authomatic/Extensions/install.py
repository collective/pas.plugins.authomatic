import logging
from Products.GenericSetup.upgrade import normalize_version

logger = logging.getLogger('pas.plugins.authomatic')


def install(portal, reinstall=False):
    setup_tool = portal.portal_setup
    portal_migration = portal.portal_migration
    version = normalize_version(
        portal_migration.getFileSystemVersion()
    ).base_version

    if int(version) < 5000:
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
