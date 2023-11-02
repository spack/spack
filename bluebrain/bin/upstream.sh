#!/usr/bin/env bash

if [ -z ${1} ]
then
    echo "Call with upstreamed package name as first argument"
    echo "It will check your current branch, checkout and update upstream/develop, then go back to your original branch."
    echo "After that it will checkout the package folder from upstream/develop, remove the patches or bluebrain version from both git and filesystem"
    echo ""
    echo "If you want to update your upstream-develop branch from upstream/develop, pass 'update' as the second argument"
    echo ""
    echo "WARNING - IF YOU HAVE ANY WORK ON upstream-develop IT WILL BE LOST"
    exit 0
fi



set -e

upstreamed=$1
update_upstream=$2

UPSTREAM_REMOTE=$(git remote -v | awk '/github.com:spack\/spack/ {print $1}' | head -n 1)

if [ -z "${UPSTREAM_REMOTE}" ]
then
    echo "upstream remote not found - adding"
    git remote add upstream github.com:spack/spack
    UPSTREAM_REMOTE=upstream
fi

if [ "${update_upstream}" == "update" ]
then
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo "Current branch is ${CURRENT_BRANCH} - updating ${UPSTREAM_REMOTE}/develop"
    git checkout -B upstream-develop --track ${UPSTREAM_REMOTE}/develop
    git pull
    git checkout ${CURRENT_BRANCH}
fi

echo "Checking out ${upstreamed} from ${UPSTREAM_REMOTE}/develop "
git checkout ${UPSTREAM_REMOTE}/develop -- var/spack/repos/builtin/packages/${upstreamed}/

ORIGINAL=""
if [ -e bluebrain/repo-patches/packages/${upstreamed} ]
then
    ORIGINAL=bluebrain/repo-patches/packages/${upstreamed}
elif [ -e bluebrain/repo-bluebrain/packages/${upstreamed} ]
then
    ORIGINAL+=" bluebrain/repo-bluebrain/packages/${upstreamed}"
fi
if [ -z ${ORIGINAL} ]
then
    echo "Original already removed"
else
    echo "Original package was in ${ORIGINAL}"
    set +e
    git rm -fr ${ORIGINAL}
    set -e
    rm -fr ${ORIGINAL}
fi

echo "All done"
