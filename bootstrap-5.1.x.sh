#!/bin/sh
ln -fs plone-5.1.x.cfg buildout.cfg
rm -r ./lib ./include ./local ./bin
virtualenv --clear .
./bin/pip install --upgrade pip setuptools zc.buildout
./bin/buildout
