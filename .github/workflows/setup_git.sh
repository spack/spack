#!/usr/bin/env sh
git config --global user.email "spack@example.com"
git config --global user.name "Test User"
# With fetch-depth: 0 we have a remote develop
# but not a local branch. Don't do this on develop
if [ "$(git branch --show-current)" != "develop" ]
then
  git branch develop origin/develop
fi
