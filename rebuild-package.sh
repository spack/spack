#!/bin/bash

set -x

echo "Building package ${SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

BUILD_CACHE_DIR=`pwd`
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"

mirrorAddResult=`spack mirror add remote_binary_mirror ${MIRROR_URL}`
echo "Attempted mirror add.  Output was:"
echo "${mirrorAddResult}"

ls -R "${BUILD_CACHE_DIR}/build_cache"

uname -a

which gcc
gcc --version

# Help spack find the compiler installed on this system
spack compiler find --scope system $(which gcc)
spack compiler find --scope system $(which g++)
spack compiler find --scope system $(which gfortran)

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
    # Now that jobs in later stages may depend on this jobs artifacts,
    # we may want to fetch the built tarball from the remote mirror at
    # this point and put it in the artifacts directory.  Or maybe the
    # install command can first look in the artifacts dir, and then on
    # the remote mirror for dependencies?
fi
