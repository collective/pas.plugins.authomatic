# Changelog
<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 2.0.0 (2025-05-15)


### Internal:

- GHA: Use plone/meta shared workflows. @ericof [#102](https://github.com/collective/pas.plugins.authomatic/issues/102)


### Documentation:

- Update README file with release instructions. @ericof 

## 2.0.0rc3 (2025-04-11)


### Bug fixes:

- Fix walrus operator usage to correctly assign authomatic_cfg() result [#100](https://github.com/collective/pas.plugins.authomatic/issues/100)

## 2.0.0rc2 (2025-04-03)


### Bug fixes:

- Add missing `plone.api` dependency. @mauritsvanrees [#95](https://github.com/collective/pas.plugins.authomatic/issues/95)

## 2.0.0rc1 (2025-03-27)


### New features:

- - Documented integration with Microsoft Entra ID @alecghica [#87](https://github.com/collective/pas.plugins.authomatic/issues/87)


### Internal:

- Add suuport to Python 3.13 @ericof [#89](https://github.com/collective/pas.plugins.authomatic/issues/89)
- Use UV to manage the environment @ericof [#90](https://github.com/collective/pas.plugins.authomatic/issues/90)
- Update .vscode configuration @ericof [#91](https://github.com/collective/pas.plugins.authomatic/issues/91)
- GHA: Update workflows. @ericof [#92](https://github.com/collective/pas.plugins.authomatic/issues/92)
- Use pytest-plone 1.0.0a1 @ericof [#93](https://github.com/collective/pas.plugins.authomatic/issues/93)

## 2.0.0b3 (2025-02-03)


### New features:

- Register the adapter as needed by the @login endpoint present in plone.restapi @erral [#73](https://github.com/collective/pas.plugins.authomatic/issues/73)


### Internal:

- Require plone.restapi higher than 9.10.0 [@ericof] 

## 2.0.0b2 (2025-01-14)


### Internal:

- Move CHANGELOG.md entries to CHANGES.md [@ericof] [#84](https://github.com/collective/pas.plugins.authomatic/issues/84)
- Document release process [@ericof] [#85](https://github.com/collective/pas.plugins.authomatic/issues/85)
- Rename logging.py to log.py [@ericof] [#86](https://github.com/collective/pas.plugins.authomatic/issues/86)

## 2.0.0b1 (2025-01-14)


### Internal:

- Modernize package repository [@ericof] [#71](https://github.com/collective/pas.plugins.authomatic/issues/71)
- Move tests to pytest [@ericof] [#72](https://github.com/collective/pas.plugins.authomatic/issues/72)
- Drop Plone 5.2 support [@ericof] [#80](https://github.com/collective/pas.plugins.authomatic/issues/80)
- Update i18n mechanism, update Brazilian Portuguese translation [@ericof] [#82](https://github.com/collective/pas.plugins.authomatic/issues/82)


## 1.4.0 (2024-12-13)


- Patch `authomatic.providers.BaseProvider._fetch` to support Python 3.12 @ericof.


## 1.3.0 (2024-11-21)

- Search users by fullname and email. @alecghica
- Fix login on Volto frontend when already logged-in in Plone Classic. @avoinea
- Add the possibility to override the ZopeRequestAdapter.
- Fix the authomatic view when it is reporting an exception that does not have a message attribute


## 1.2.0 (2023-09-13)

- Add Spanish translation. @macagua

- Better handle values from identity data. @cekk

- Add `username_userid` User ID factory. @ericof

- Annotate transaction in POST calls to authenticate a user. @ericof


## 1.1.2 (2023-03-15)

- Support Python 3.11 for Plone 6. @ericof

- Lint fixes @ericof


## 1.1.1 (2022-10-14)

- Upgrade plone/code-analysis-action to version 2. @ericof

- Fix packaging issue related to CHANGELOG.md not being included in the source package. @ericof

- Support Python 3.10 for Plone 6. @ericof


## 1.1.0 (2022-10-10)

- Add the plone.restapi adapter to show the controlpanel in Volto. @erral

- Add possibility to redirect to `next_url` via provided cookie @avoinea


## 1.0.0 (2022-07-25)

- Use plone/plone-setup GitHub Action. @ericof

- Add Brazilian Portuguese translation. @ericof

- Use plone/code-analysis-action GitHub Action for code analysis. @ericof

- Fix doChangeUser takes 2 positional arguments but 3 were given @avoinea

## 1.0b2 (2021-08-18)

- Fix tox setup, move CI from TravisCI to GitHub Actions. @jensens

- Code Style Black, Isort, zpretty and Pyupgrade applied. @jensens

- Add missing no-op methods for IUserManagement to plugin.
  This fixes the tests. @jensens

- Drop Python 2 support and so require Plone 5.2. @jensens

- Include permissions from CMFCore to avoid ComponentLookupError. @bsuttor

- Fixed ModuleNotFoundError: No module named 'App.class_init' on Zope 5. @bsuttor

- Add french translation @mpeeters

- PAS event notification IPrincipalCreatedEvent. @jensens

- Python 3 and Plone 52 compatibility. @cekk

- Fix #44: Fullfill strictly exact_match when enumerating users @allusa

- Allow users deletion. @cekk

- Drop Plone < 5.1.x compatibility. @cekk

- Fix #54: Notification of PrincipalCreated event. @ericof

- Closes #55: Support plone.restapi. @ericof

## 1.0b1 (2017-11-20)

- Slighly beautify login modal. @jensens

- Fix #33" Page does not exist Control Settings. @jensens

- Fix #31: Link is broken to JSON configuration documentation in help text. @jensens

- Fix #28: After uninstall plone.external_login_url is still registered and the login broken. @jensens

- Support for Plone 5.1 tested (worked, ust control-panel icon needed some tweak).
  Buildout configuration for 5.1 added. @jensens

- Install: Hide non-valid profiles at install form. @jensens

- Additional checks to ensure to never have an empty/None key stored. @jensens

- Fix #27: Update user data after login. @jensens

- Fix filter users bug in enumerateUsers plugin where it was always returning
  all the users. @sneridagh

- fix typo and wording of login message @tkimnguyen


## 1.0a7 (2016-02-15)

- Workaround for None users. @sneridagh


## 1.0a6 (2016-01-11)

- Fix #21: When you logout and then login again, a new user is created. @jensens


## 1.0a5 (2015-12-04)

- Fix: #18 "Provider Login" option for "Generator for Plone User ID" seems
  broken @jensens

- Fix: Title indicates if an identity is added @jensens

- Fix: Correct usage of plone.protect @jensens


## 1.0a4 (2015-11-20)

- Added german translation @jensens

- Restored Plone 4 compatibility @keul

- Added italian translation @keul

- Proper uninstall @keul

## 1.0a3 (2015-11-15)

- Refactor authomatic-handler to enable adding identities. @jensens

- Fix: use secret from settings as secret for Authomatic. @jensens

- Renamed view ``authomatic-login`` to ``authomatic-handler``, because this
  view will be used to add an identity too (url must be registered on provider
  side sometimes and we want to do this only once). @jensens


## 1.0a2 (2015-11-14)

- Minimal validation of JSON. @jensens

- Make the whole ``remember`` procedure a ``safeWrite`` if called from login
  view. We can not pass a authenticator token here, because of redirects and
  expected return urls . @jensens

- Allow selection of user id generator strategy. @jensens

- Allow multiple services for one user. This changes a lot behind the scenes. @jensens

- Use authomatic.core.User attributes instead of raw provider data. closes [#9](https://github.com/collective/pas.plugins.authomatic/issues/9) @ericof


## 1.0a1 (2015-10-28)

- Initial release.
