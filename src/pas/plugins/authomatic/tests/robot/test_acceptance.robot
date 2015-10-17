# ============================================================================
# MEMBERPROPERTY TO GROUP ACCEPTANCE TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s pas.plugins.authomatic -t test_acceptance.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src pas.plugins.authomatic.testing.PAS_PLUGINS_Authomatic_PLONE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/pas/plugins/authomatic/tests/robot/test_acceptance.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

