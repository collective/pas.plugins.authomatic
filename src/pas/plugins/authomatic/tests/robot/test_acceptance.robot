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

Scenario: As administrator I can create a group based on member properties
  Given a user with the property 'usertype' = 'employee'
    and a logged-in manager
   When I create a virtual group 'Employees' with the property 'usertype' = 'employee'
   Then the user is member of the group 'Employees'

Scenario: As reviewer I can grant permissions based on member properties groups
  Given a user with the property 'usertype' = 'employee'
    and a virtual group 'Employees' with the property 'usertype' = 'employee'
    and a logged-in manager
   When I grant the virtual group 'Employees' the 'Edit' permission on a folder
   Then the user can edit the folder

Scenario: As administrator I can create a group based on multiple member properties
  Pass Execution  Not implemented yet
  Given a user 'John Doe' with the property 'usertype' = 'employee'
    and a user 'Jane Doe' with the property 'city' = 'bonn'
    and a logged-in manager
   When I create a virtual group 'Employees' with the property 'usertype' = 'employee'
    and I create a virtual group 'Locals' with the property 'city' = 'bonn'
   Then the user 'John Doe' is member of the group 'Employees'
    and the user 'Jane Doe' is member of the group 'Locals'

Scenario: As administrator I can create a group based on member properties prefixes
  Given a user with the property 'student_id' = '1234567'
    and a logged-in manager
   When I create a virtual group 'Students' with the property 'student_id' = '123*'
   Then the user is member of the group 'Students'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in manager
  Enable Autologin As  Manager

a logged-in reviewer
  Enable Autologin As  Reviewer

a user with the property '${property}' = '${value}'
  Go To  ${PLONE_URL}

a user '${user}' with the property '${property}' = '${value}'
  Go To  ${PLONE_URL}

a virtual group '${group}' with the property '${property}' = '${value}'
  Enable autologin as  Manager
  Go to  ${PLONE_URL}/@@authomatic-controlpanel
  Input text  form.widgets.group_property  ${property}
  Input text  form.widgets.valid_groups  ${value}|${group}|${group}|${group} (Virtual Group)|my-virtual-group@example.com
  Click button  Save
  Wait until page contains  Changes saved


# --- WHEN -------------------------------------------------------------------

I create a virtual group '${group}' with the property '${property}' = '${value}'
  Go to  ${PLONE_URL}/@@authomatic-controlpanel
  Input text  form.widgets.group_property  ${property}
  Input text  form.widgets.valid_groups  ${value}|${group}|${group}|${group} (Virtual Group)|my-virtual-group@example.com
  Capture screenshot  authomatic-controlpanel.png
  Click button  Save
  Wait until page contains  Changes saved

I grant the virtual group '${group}' the 'Edit' permission on a folder
  Create content  type=Folder  id=folder  title=Folder
  Go to  ${PLONE_URL}/folder/@@sharing
  Wait until page contains element  css=#sharing-user-group-search
  Input text  css=#sharing-user-group-search  ${group}
  Click button  css=#sharing-search-button
  Xpath Should Match X Times  //table[@id='user-group-sharing']//td[@title='${group}']  1
  Select checkbox  xpath=//table[@id='user-group-sharing']//td[@title='Employees']/following-sibling::td[2]/input
  Capture screenshot  grant-virtual-group-permission-on-folder.png
  Click button  Save
  Wait until page contains  Changes saved


# --- THEN -------------------------------------------------------------------

the user is member of the group '${group}'
  Go To  ${PLONE_URL}/@@usergroup-usermembership?userid=test_user_1_
  Wait until page contains  Current group memberships
  Xpath Should Match X Times  //table[@summary='Group Memberships Listing']//tr/td//*[text()[contains(., '${group}')]]  1
  Capture screenshot  the-user-is-member-of-the-group.png

the user can edit the folder
  Disable autologin
  Enable autologin as  test_user_1_
  Go to  ${PLONE_URL}/folder
  Click element  xpath=//*[contains(text(), 'Edit')]
  Wait until page contains  Site Map
  Page should contain  Edit
  Page should contain element  xpath=//*[@value='Save']
  Capture screenshot  the-user-can-edit-the-folder.png


# --- HELPER -----------------------------------------------------------------

Capture screenshot
  [Arguments]  ${filename}
  # Base path is '/parts/test/test_acceptance/Scenario_[...]/
  Capture Page Screenshot  filename=../../../../docs/source/_screenshots/${filename}
