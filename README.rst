.. image:: https://travis-ci.org/collective/pas.plugins.authomatic.svg?branch=master
    :target: https://travis-ci.org/collective/pas.plugins.authomatic

.. image:: https://coveralls.io/repos/collective/pas.plugins.authomatic/badge.svg
  :target: https://coveralls.io/r/collective/pas.plugins.authomatic


.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.


=============================================================================
pas.plugins.authomatic
=============================================================================


Features
--------

  - Integration of different OAuth Providers
  - For now only Github is integrated


Documentation
-------------

  - This Package will create a View called authomatic-login where you can login with different Providers
  - The Provider is choosen in the URL so if you call */authomatic-login/github you will use Github to Login
  - Example JSON Configuration 
    {
    "github": {
        "class_": "authomatic.providers.oauth2.GitHub",
        "consumer_key": "xxxx",
        "consumer_secret": "xxxxx"
    }
}

Installation
------------

Install pas.plugins.authomatic by adding it to your buildout::

   [buildout]

    ...

    eggs =
        authomatic
        pas.plugins.authomatic


and then running "bin/buildout".


Contribute
----------

- `Source code at Github <https://github.com/collective/pas.plugins.authomatic>`_
- `Issue tracker at Github <https://github.com/collective/pas.plugins.authomatic/issues>`_

Support
-------

If you are having issues, `please let us know <https://github.com/collective/pas.plugins.authomatic/issues>`_.


Development
-----------

Plone 4
    There must be an ``python`` binary available in system path pointing to Python 2.7 , then::

        $ bootstrap-4.3.x.sh

Plone 5
    There must be an ``python`` binary available in system path pointing to Python 2.7 , then::

        $ bootstrap-5.0.x.sh


License
-------

The project is licensed under the GPLv2.
