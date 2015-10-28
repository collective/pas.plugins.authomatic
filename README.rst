.. image:: https://travis-ci.org/collective/pas.plugins.authomatic.svg?branch=master
    :target: https://travis-ci.org/collective/pas.plugins.authomatic

.. image:: https://coveralls.io/repos/collective/pas.plugins.authomatic/badge.svg?branch=master&service=github 
    :target: https://coveralls.io/github/collective/pas.plugins.authomatic?branch=master 


.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.


=============================================================================
Login with OAuth2/ OpenId by integrating Authomatic in Plone
=============================================================================

**pas.plugins.authomatic**

Features
--------

Provides OAuth2 and OpenID login capability for Plone:

It integrates the awesome `Authomatic <http://peterhudec.github.io/authomatic/index.html>`_ package in Plone

  Authomatic is a framework agnostic library
  for Python web applications
  with a minimalistic but powerful interface
  which simplifies authentication of users
  by third party providers like Facebook or Twitter
  through standards like OAuth and OpenID.

  *by Author Peter Hudec on Authomatic website*

It has out of the box support for:

OAuth 1.0a providers
    Bitbucket, Flickr, Meetup, Plurk, Twitter, Tumblr, UbuntuOne, Vimeo, Xero, Xing and Yahoo.
OAuth 2.0 providers
    Amazon, Behance, Bitly, Cosm, DeviantART, Eventbrite, Facebook, Foursquare, GitHub, Google, LinkedIn, PayPal, Reddit, Viadeo, VK, WindowsLive, Yammer and Yandex.
OpenID
    python-openid and Google App Engine based OpenID.


Documentation
-------------

- This package will create a view called ``authomatic-login`` where you can login with different providers
- The provider is choosen in the URL so if you call ``/authomatic-login/PROVIDER`` you will use PROVIDER to login
- You can set the JSON configuration of the plugin in the Controlpanel ``@@authomatic-controlpanel`` (linked under security)
- Example JSON configuration (first level key is the PROVIDER::

    {
        "github": {
            "display": {
                "title": "Github",
                "cssclasses": {
                    "button": "btn btn-default",
                    "icon": "glypicon glyphicon-github"
                },
                "as_form": false
            },
            "propertymap": {
                "email": "email",
                "link": "home_page",
                "location": "location",
                "name": "fullname"
            },
            "class_": "authomatic.providers.oauth2.GitHub",
            "consumer_key": "5c4901d141e736f114a7",
            "consumer_secret": "d4692ca3c0ab6cc1f8b28d3ccb1ea15b61e7ef5c",
            "access_headers": {
                "User-Agent": "Plone Authomatic Plugin"
            }
        },
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

Start Plone and activate the plugin in the addons control-panel.

Go to the Authomatic controlpanel (security section) and configure the plugin.

Configuration parameters for the different authorization are provided as JSON text in there.
JSON is used because of flexibility.
Details at `Authomatics provider section <http://peterhudec.github.io/authomatic/reference/providers.html>`_.

There are some differences in configuration:

- the value of ``"class_"`` has to be a string, which is then resolved as a dotted path.
- each provider can get an optional entry ``display`` with sub-enties such as:

  - ``title`` which is used in the templates instead of the section name.
  - ``iconclasses`` which is applied in the templates to an span.
  - ``buttonclasses`` which is applied in the templates to the button.
  - ``as_form`` (true/false) which renders a form for OpenId providers.

- each provider can get an optional entry ``propertymap``.
  It is a mapping from authomatic/provider user properties to plone user properties, like ``"fullname": "name",``.
  Look at each providers documentation which properties are available.

Source Code and Contributions
-----------------------------

If you want to help with the development (improvement, update, bug-fixing, ...) of ``pas.plugins.authomatic`` this is a great idea!

- `Source code at Github <https://github.com/collective/pas.plugins.authomatic>`_
- `Issue tracker at Github <https://github.com/collective/pas.plugins.authomatic/issues>`_

You can clone it or `get access to the github-collective <http://collective.github.com/>`_ and work directly on the project.
Please do larger changes on a branch and submit a Pull Request.

Maintainer of pas.plugins.authomatic is Jens Klein.
We appreciate any contribution and if a release is needed to be done on pypi, please just contact one of us.

Development
-----------

There must be an ``python`` binary available in system path pointing to Python 2.7.
Also you need to have all installed to develop with Plone (see http://docs.plone.org/) then:

- Plone 4: ``bootstrap-4.3.x.sh``
- Plone 5: ``$ bootstrap-4.3.x.sh``


License
-------

The project is licensed under the GPLv2.

