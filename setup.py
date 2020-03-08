# -*- coding: utf-8 -*-
"""Installer for the pas.plugins.authomatic package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() + '\n' + 'Contributors\n'
    '============\n'
    + '\n'
    + open('CONTRIBUTORS.rst').read()
    + '\n'
    + open('CHANGES.rst').read()
    + '\n'
)


setup(
    name='pas.plugins.authomatic',
    version='1.0b2.dev0',
    description='Provides OAuth2/ OpenID login for Plone using Authomatic.',
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
    ],
    keywords='Python Plone PAS OAuth',
    author='Jens Klein and Matthias Dollfuss',
    author_email='dev@bluedynamics.com',
    url='http://pypi.python.org/pypi/pas.plugins.authomatic',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['pas', 'pas.plugins'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'authomatic>=0.2.0a3',
        'Plone',
        'plone.api',
        'plone.protect>=3.0.0',  # plone4.csrffixes will include this
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
