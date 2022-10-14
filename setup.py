"""Installer for the pas.plugins.authomatic package."""
from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CHANGELOG.md").read_text()}\n
"""

setup(
    name="pas.plugins.authomatic",
    version="1.1.1",
    description="Provides OAuth2/OpenID login for Plone using Authomatic.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "Framework :: Zope :: 5",
        "Framework :: Zope",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python",
    ],
    keywords="Python Plone PAS OAuth Authentication",
    author="Jens Klein and Matthias Dollfuss",
    author_email="dev@bluedynamics.com",
    url="https://github.com/collective/pas.plugins.authomatic",
    project_urls={
        "Repository": "https://github.com/collective/pas.plugins.authomatic/",
        "Changelog": "https://github.com/collective/pas.plugins.authomatic/blob/main/CHANGELOG.md",  # noQA
        "Issues": "https://github.com/collective/pas.plugins.authomatic/issues",
    },
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["pas", "pas.plugins"],
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    zip_safe=False,
    install_requires=[
        "authomatic>=1.0.0",
        "Products.CMFPlone>=5.2",
        "plone.restapi",
        "setuptools",
    ],
    extras_require={
        "test": [
            "collective.MockMailHost",
            "parameterized",
            "plone.app.testing",
            "plone.restapi[test]",
            "plone.app.robotframework[debug]",
            "zest.releaser[recommended]",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = pas.plugins.authomatic.locales.update:update_locale
    """,
)
