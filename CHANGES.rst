Changelog
=========

1.0b2 (unreleased)
------------------

- Add french translation
  [mpeeters]

- PAS event notification IPrincipalCreatedEvent.
  [jensens]

- Python 3 and Plone 52 compatibility.
  [cekk]

1.0b1 (2017-11-20)
------------------

- Slighly beautify login modal.
  [jensens]

- Fix #33" Page does not exist Control Settings.
  [jensens]

- Fix #31: Link is broken to JSON configuration documentation in help text.
  [jensens]

- Fix #28: After uninstall plone.external_login_url is still registered and the login broken.
  [jensens]

- Support for Plone 5.1 tested (worked, ust control-panel icon needed some tweak).
  Buildout configuration for 5.1 added.
  [jensens]

- Install: Hide non-valid profiles at install form.
  [jensens]

- Additional checks to ensure to never have an empty/None key stored.
  [jensens]

- Fix #27: Update user data after login.
  [jensens]

- Fix filter users bug in enumerateUsers plugin where it was always returning
  all the users.
  [sneridagh]

- fix typo and wording of login message [tkimnguyen]


1.0a7 (2016-02-15)
------------------

- Workaround for None users.
  [sneridagh]


1.0a6 (2016-01-11)
------------------

- Fix #21: When you logout and then login again, a new user is created.
  [jensens]


1.0a5 (2015-12-04)
------------------

- Fix: #18 "Provider Login" option for "Generator for Plone User ID" seems
  broken
  [jensens]

- Fix: Title indicates if an identity is added
  [jensens]

- Fix: Correct usage of plone.protect
  [jensens]


1.0a4 (2015-11-20)
------------------

- Added german translation
  [jensens]

- Restored Plone 4 compatibility
  [keul]

- Added italian translation
  [keul]

- Proper uninstall
  [keul]

1.0a3 (2015-11-15)
------------------

- Refactor authomatic-handler to enable adding identities.
  [jensens]

- Fix: use secret from settings as secret for Authomatic.
  [jensens]

- Renamed view ``authomatic-login`` to ``authomatic-handler``, because this
  view will be used to add an identity too (url must be registered on provider
  side sometimes and we want to do this only once).
  [jensens]


1.0a2 (2015-11-14)
------------------

- Minimal validation of JSON.
  [jensens]

- Make the whole ``remember`` procedure a ``safeWrite`` if called from login
  view. We can not pass a authenticator token here, because of redirects and
  expected return urls .
  [jensens]

- Allow selection of user id generator strategy.
  [jensens]

- Allow multiple services for one user. This changes a lot behind the scenes.
  [jensens]

- Use authomatic.core.User attributes instead of raw provider data. closes `#9`_
  [ericof]


1.0a1 (2015-10-28)
------------------

- Initial release.


.. _`#9`: https://github.com/collective/pas.plugins.authomatic/issues/9
