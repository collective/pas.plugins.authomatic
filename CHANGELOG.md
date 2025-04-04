# Changelog

## 1.4.1 (2025-04-04)


- Restore compatibility with Plone 6.0.15. Fixes [#97](https://github.com/collective/pas.plugins.authomatic/issues/97). @ale-rt


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
