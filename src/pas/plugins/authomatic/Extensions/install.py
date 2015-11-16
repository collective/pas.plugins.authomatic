from Products.GenericSetup.upgrade import normalize_version

import logging

logger = logging.getLogger('pas.plugins.authomatic')


def install(portal, reinstall=False):
    setup_tool = portal.portal_setup
    portal_migrations = portal.portal_migration
    versions = portal_migrations.coreVersions()
    version = normalize_version(
        portal_migrations.getFileSystemVersion()
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
