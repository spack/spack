#!/bin/bash -e
git config --global user.email "spack@example.com"
git config --global user.name "Test User"

# See https://github.com/git/git/security/advisories/GHSA-3wp6-j8xr-qw85 (CVE-2022-39253)
# This is needed to let some fixture in our unit-test suite run
git config --global protocol.file.allow always

# create a local pr base branch
if [[ -n $GITHUB_BASE_REF ]]; then
    git fetch origin "${GITHUB_BASE_REF}:${GITHUB_BASE_REF}"
fi
