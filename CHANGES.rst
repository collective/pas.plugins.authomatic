Changelog
=========

1.0a3 (unreleased)
------------------

- Refacor authomatic-handler to enable adding identities.
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
