#!/usr/bin/env sh
git config --global user.email "spack@example.com"
git config --global user.name "Test User"

# create a local pr base branch
if [[ -n $GITHUB_BASE_REF ]]; then
    git branch "${GITHUB_BASE_REF}" "origin/${GITHUB_BASE_REF}"
fi
