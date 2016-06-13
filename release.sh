#!/bin/bash

# stash anything not committed to git
git stash save --include-untracked "Stash before release"

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

# reapply stashed changes from git
git stash pop
