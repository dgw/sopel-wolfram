#!/bin/bash

# stash anything not committed to git
old_stash=$(git rev-parse -q --verify refs/stash)
git stash save -q --include-untracked "Stash before release"
new_stash=$(git rev-parse -q --verify refs/stash)

# remove old distributions (if any)
rm dist/*

# generate new distributions

## source distribution
## PyPI only allows one format, so use the most common (.tar.gz)
python setup.py sdist --formats=gztar

## binary wheels
### universal
python setup.py bdist_wheel --universal
### py2
python setup.py bdist_wheel
### py3
python3 setup.py bdist_wheel

# upload distributions

twine upload dist/*

# reapply stashed changes from git only if pre-release stash was non-empty
if [ "$old_stash" != "$new_stash" ]; then
    git stash pop -q
fi
