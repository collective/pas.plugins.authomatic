# -*- coding: utf-8 -*-
"""Installer for the pas.plugins.authomatic package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)


setup(
    name="pas.plugins.authomatic",
    version="1.0b2.dev0",
    description="Provides OAuth2/ OpenID login for Plone using Authomatic.",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        #        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="Python Plone PAS OAuth",
    author="Jens Klein and Matthias Dollfuss",
    author_email="dev@bluedynamics.com",
    url="https://github.com/collective/pas.plugins.authomatic",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["pas", "pas.plugins"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "authomatic>=1.0.0",
        "Products.CMFPlone>=5.2",
        "setuptools",
    ],
    extras_require={
        "test": [
            "collective.MockMailHost",
            "plone.app.testing",
            "plone.app.robotframework[debug]",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
