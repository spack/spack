#!/bin/bash

set -ex

### This script may first contact the remote mirror (MIRROR_URL) to
### find out whether the build is actually necessary.

echo "Building package ${SPEC_NAME}, ${SHORT_HASH}, ${MIRROR_URL}"

BUILD_CACHE_DIR=`pwd`
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"

checkResult=`spack check-binaries single --spec "${SPEC_NAME}" --mirror-url "${MIRROR_URL}"`

upToDateRegex="up to date$"

if ! [[ "$checkResult" =~ $upToDateRegex ]]; then
    # First build/install the package
    # buildResult=`spack install "${SPEC_NAME}"`
    spack install "${SPEC_NAME}"

    # Now create a buildcache entry, might not work w/out a mirror set up
    # cacheResult=`spack buildcache create -a -f -d "${BUILD_CACHE_DIR}" "${SPEC_NAME}"`
    spack buildcache create -u -a -f -d "${BUILD_CACHE_DIR}" "${SPEC_NAME}"

    # Now push buildcache entry to remote mirror
    ls -al "${BUILD_CACHE_DIR}/build_cache"
else
    echo "spec ${SPEC_NAME} is already up to date"
fi
