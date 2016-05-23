#!/bin/bash

# remove old distributions (if any)
rm dist/*

# generate new distributions

## source distributions for *nix & Windows
python setup.py sdist --formats=gztar,zip

## binary wheels
### universal
python setup.py bdist_wheel --universal
### py2
python setup.py bdist_wheel
### py3
python3 setup.py bdist_wheel

# upload distributions

twine upload dist/*
