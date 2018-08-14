#!/bin/bash

set -x

echo "Building package ${SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

BUILD_CACHE_DIR=`pwd`
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"

mirrorAddResult=`spack mirror add remote_binary_mirror ${MIRROR_URL}`
echo "Attempted mirror add.  Output was:"
echo "${mirrorAddResult}"

# spack buildcache check --spec "${SPEC_NAME}" --mirror-url "${MIRROR_URL}" --no-index
spack buildcache check --spec "${SPEC_NAME}" --no-index

if [[ $? -ne 0 ]]; then
    spack install "${SPEC_NAME}"

    spack buildcache create -u -a -f -d "${BUILD_CACHE_DIR}" "${SPEC_NAME}"

    # Now push buildcache entry to remote mirror, something like:
    # "spack buildcache put <mirror> <spec>", when that subcommand
    # is implemented
    ls -al "${BUILD_CACHE_DIR}/build_cache"
else
    echo "spec ${SPEC_NAME} is already up to date"
fi
