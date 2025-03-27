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

## Features

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

### Supported Providers

Out of the box,  **pas.plugins.authomatic** supports the following providers

#### OAuth 1.0

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

#### OAuth 2.0

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

#### OpenID

- python-openid
- Google App Engine based OpenID.


## Documentation

This package supports Plone sites using Volto or the Classic UI.

### Volto Frontend

- Endpoint `@login` with GET: Returns list of authentication options
- Endpoint `@login-authomatic` with GET: Provide information to start the OAuth process.
- Endpoint `@login-authomatic` with POST: Handles OAuth login and returns a JSON web token (JWT).
- For Volto sites you must also install [@plone-collective/volto-authomatic](https://github.com/collective/volto-authomatic).
- Plugin configuration is available in the Control-panel `/controlpanel/authomatic` (linked under users)
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

### Classic UI

- This package creates a view called `authomatic-handler` where you can login with different providers.
- The view can be used as well to add an identity from a provider to an existing account.
- The provider is choosen in the URL so if you call `/authomatic-handler/PROVIDER` you will use PROVIDER to login.
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

## Installation

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

## Configuration

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

## Integration with Entra ID

Enumeration PAS plugin: if you're using **pas.plugins.authomatic** with *Microsoft Entra ID*, we recommend pairing it with [pas.plugins.eea](https://github.com/eea/pas.plugins.eea) for proper user enumeration and metadata synchronization. This complementary plugin enables listing all the Entra ID users and groups and is compatible with both Plone 5 and Plone 6.

## Source Code and Contributions

If you want to help with the development (improvement, update, bug-fixing, ...) of `pas.plugins.authomatic` this is a great idea!

- [Issue Tracker](https://github.com/collective/pas.plugins.authomatic/issues)
- [Source Code](https://github.com/collective/pas.plugins.authomatic/)

Please do larger changes on a branch and submit a Pull Request.

Creator of **pas.plugins.authomatic** is Jens Klein.

We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.

### Development

You need a working `python` environment (system, virtualenv, pyenv, etc) version 3.7 or superior.

Then install the dependencies and a development instance using:

```bash
make install
```

To run tests for this package:

```bash
make test
```

To lint the codebase:

```bash
make lint
```

By default we use the latest Plone version in the 6.x series.

### Changelog entries

The `CHANGES.md` file is managed using [towncrier](https://towncrier.readthedocs.io/). All non trivial changes must be accompanied by an entry in the `news` directory. Using such a tool instead of editing the file directly, has the following benefits:

* It avoids merge conflicts in CHANGES.md.
* It avoids news entries ending up under the wrong version header.

The best way of adding news entries is this:

* First create an issue describing the change you want to make. The issue number serves as a unique indicator for the news entry. As example, let's say you have created issue 42.

* Create a file inside of the news/ directory, named after that issue number:

  * For bug fixes: 42.bugfix.
  * For new features: 42.feature.
  * For internal changes: 42.internal.
  * For breaking changs: 42.breaking.
  * Any other extensions are ignored.

* The contents of this file should be markdown formatted text that will be used as the content of the CHANGES.md entry.

Towncrier will automatically add a reference to the issue when rendering the CHANGES.md file.

### Releasing `pas.plugins.authomatic`

Releasing `pas.plugins.authomatic` is done using a combination of [zest.releaser](https://zestreleaser.readthedocs.io/) and [hatch](https://hatch.pypa.io/latest/).

The release process consists of three steps: **Pre-release**, **Release**, and **Post-release**.

#### Pre-release
Run the following command to populate the `CHANGES.md` file with the entries available in the `news/` directory:

```bash
.venv/bin/prerelease
```

#### Release

1. Create a new Git tag:
   ```bash
   git tag -a {VERSION} -m "Release {VERSION}"
   ```
2. Build the project:
   ```bash
   hatch build
   ```
3. Publish the package to PyPI:
   ```bash
   hatch publish
   ```

#### Post-release
Run the following command to bump the package version, create a new commit, and push all changes to GitHub:

```bash
.venv/bin/postrelease
```

## License

The project is licensed under the GPLv2.
