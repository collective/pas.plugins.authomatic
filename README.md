<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/collective/pas.plugins.authomatic/main/docs/authomatic.svg" width="70" /></div>

<h1 align="center">OAuth2 / OpenId Authentication in Plone</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pas.plugins.authomatic)](https://pypi.org/project/pas.plugins.authomatic/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pas.plugins.authomatic)](https://pypi.org/project/pas.plugins.authomatic/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pas.plugins.authomatic)](https://pypi.org/project/pas.plugins.authomatic/)
[![PyPI - License](https://img.shields.io/pypi/l/pas.plugins.authomatic)](https://pypi.org/project/pas.plugins.authomatic/)
[![PyPI - Status](https://img.shields.io/pypi/status/pas.plugins.authomatic)](https://pypi.org/project/pas.plugins.authomatic/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/pas.plugins.authomatic)](https://pypi.org/project/pas.plugins.authomatic/)

[![Code analysis checks](https://github.com/collective/pas.plugins.authomatic/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/collective/pas.plugins.authomatic/actions/workflows/code-analysis.yml)
[![Tests](https://github.com/collective/pas.plugins.authomatic/actions/workflows/tests.yaml/badge.svg)](https://github.com/collective/pas.plugins.authomatic/actions/workflows/tests.yaml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/pas.plugins.authomatic)](https://github.com/collective/pas.plugins.authomatic)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/pas.plugins.authomatic?style=social)](https://github.com/collective/pas.plugins.authomatic)

</div>

Features
--------

**pas.plugins.authomatic** provides OAuth2 and OpenID login capability for Plone sites by integrating the awesome [Authomatic](https://authomatic.github.io/authomatic/) package.

```
Authomatic is a framework agnostic library
for Python web applications
with a minimalistic but powerful interface
which simplifies authentication of users
by third party providers like Facebook or Twitter
through standards like OAuth and OpenID.
```
*by author Peter Hudec on Authomatic website*


Supported Providers
-------------------

Out of the box,  **pas.plugins.authomatic** supports the following providers

*OAuth 1.0a*

- Bitbucket
- Flickr
- Meetup
- Plurk
- Twitter
- Tumblr
- UbuntuOne
- Vimeo
- Xero
- Xing
- Yahoo

*OAuth 2.0*

- Amazon
- Behance
- Bitly
- Cosm
- DeviantART
- Eventbrite
- Facebook
- Foursquare
- GitHub
- Google
- LinkedIn
- PayPal
- Reddit
- Viadeo
- VK
- WindowsLive
- Yammer
- Yandex

*OpenID*

- python-openid
- Google App Engine based OpenID.


Documentation
-------------

This package supports Plone sites using Volto or the Classic UI.

For the Classic UI:

- This package creates a view called `authomatic-handler` where you can login with different providers.
- The view can be used as well to add an identity from a provider to an existing account.
- The provider is choosen in the URL so if you call `/authomatic-handler/PROVIDER` you will use PROVIDER to login.

For Volto:

- Endpoint `@login` with GET: Returns list of authentication options
- Endpoint `@login-authomatic` with GET: Provide information to start the OAuth process.
- Endpoint `@login-authomatic` with POST: Handles OAuth login and returns a JSON web token (JWT).
- For Volto sites you must also install [@plone-collective/volto-authomatic](https://github.com/collective/volto-authomatic).


Configuration is, currently, done via Classic UI:

- Plugin configuration is available in the Controlpanel `@@authomatic-controlpanel` (linked under users)
- Example JSON configuration (first level key is the PROVIDER):

```json
{
  "github": {
    "display": {
      "title": "Github",
      "cssclasses": {
          "button": "plone-btn plone-btn-default",
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
```

Installation
------------

Add **pas.plugins.authomatic** to the Plone installation using `pip`:

```bash
pip install pas.plugins.authomatic
```
or add it as a dependency on your package's `setup.py`

```python
    install_requires = [
        "pas.plugins.authomatic",
        "Products.CMFPlone",
        "plone.restapi",
        "setuptools",
    ],
```

Start Plone and activate the plugin in the addons control-panel.

Configuration
-------------

Using Classic UI, go to the `Authomatic` controlpanel.

<img alt="Screenshot" src="https://raw.githubusercontent.com/collective/pas.plugins.authomatic/main/docs/plone-control-panel.png" width="300" />

Configuration parameters for the different authorization are provided as JSON text in there. We use JSON because of its flexibility.

<img alt="Screenshot" src="https://raw.githubusercontent.com/collective/pas.plugins.authomatic/main/docs/plugin-settings.png" width="300" />

Details about the configuration of each provider can be found at [Authomatic provider section](https://authomatic.github.io/authomatic/reference/providers.html).

There are some differences in configuration:

- Value of `"class_"` has to be a string, which is then resolved as a dotted path.
- Each provider can get an optional entry `display` with sub-enties such as:

  - `title` which is used in the templates instead of the section name.
  - `iconclasses` which is applied in the templates to an span.
  - `buttonclasses` which is applied in the templates to the button.
  - `as_form` (true/false) which renders a form for OpenId providers.

- Each provider can get an optional entry `propertymap`.
  It is a mapping from authomatic/provider user properties to plone user properties, like `"fullname": "name",`. Look at each providers documentation which properties are available.


Source Code and Contributions
-----------------------------

If you want to help with the development (improvement, update, bug-fixing, ...) of `pas.plugins.authomatic` this is a great idea!

- [Issue Tracker](https://github.com/collective/pas.plugins.authomatic/issues)
- [Source Code](https://github.com/collective/pas.plugins.authomatic/)


Please do larger changes on a branch and submit a Pull Request.

Creator of **pas.plugins.authomatic** is Jens Klein.

We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.

Development
-----------

You need a working `python` environment (system, virtualenv, pyenv, etc) version 3.7 or superior.

Then install the dependencies and a development instance using:

```bash
make build
```

To run tests for this package:

```bash
make test
```

By default we use the latest Plone version in the 6.x series.

License
-------

The project is licensed under the GPLv2.
