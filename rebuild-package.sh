#!/bin/bash

set -x

echo "Building package ${SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

CURRENT_WORKING_DIR=`pwd`
LOCAL_MIRROR="${CURRENT_WORKING_DIR}/local_mirror"
BUILD_CACHE_DIR="${LOCAL_MIRROR}/build_cache"
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"

# Make the build_cache directory if it doesn't exist
mkdir -p "${BUILD_CACHE_DIR}"

# Configure mirrors.  The first is the remote binary mirror
# we want to update, the second is a local mirror where build
# artifacts are created and then later consumed as dependencies.
# Here we're counting on mirror precedence:
#     https://spack.readthedocs.io/en/latest/mirrors.html#mirror-precedence
# so that we first check the local mirror (the artifacts generated
# by jobs in previous stages), and then the remote mirror.  Looking
# at the "mirror add" code, however, it seems new mirrors are inserted
# in the list at position zero.
spack mirror add remote_binary_mirror ${MIRROR_URL}
spack mirror add local_artifact_mirror "file://${LOCAL_MIRROR}"

# Now that we have mirrors configured, attempt to download and trust
# keys from that mirror.
# spack buildcache keys --install --trust --force

# (
#     ( echo "${SPACK_PUBLIC_KEY}" | tr -d ' \n' | base64 -d ) &&
#     echo &&
#     ( echo "${SPACK_PRIVATE_KEY}" | tr -d ' \n' | base64 -d )
# ) > ./keystuff.key

# ( echo "${SPACK_PRIVATE_KEY}" | tr -d ' \n' | base64 -d ) > ./keystuff.key

# spack gpg trust ./keystuff.key

# spack gpg list --signing
# spack gpg list --trusted

# spack gpg trust echo "$SPACK_PUBLIC_KEY" | tr -d ' \n' | base64 -d

# Finally, we can check the spec we have been tasked with build against
# the built binary on the remote mirror to see if it needs to be rebuilt
spack buildcache check --spec "${SPEC_NAME}" --mirror-url "${MIRROR_URL}" --no-index

if [[ $? -ne 0 ]]; then
    # May need to trust buildcache keys here, so that the "--use-cache"
    # flag to install works for getting built dependencies from the mirror
    #spack buildcache keys -y

    spack install --use-cache "${SPEC_NAME}"

    # buildcache_create_cmd="spack -d buildcache create -a -f "

    # if [ -n "${SIGN_KEY_HASH}" ]
    # then
    #     buildcache_create_cmd="${buildcache_create_cmd} -k ${SIGN_KEY_HASH}"
    # fi

    # buildcache_create_cmd="${buildcache_create_cmd} -d ${LOCAL_MIRROR} \\"${SPEC_NAME}\\""

    # `${buildcache_create_cmd}`

    spack buildcache create -u -a -f -d "${LOCAL_MIRROR}" "${SPEC_NAME}"

    # Now push buildcache entry to remote mirror, something like:
    # "spack buildcache put <mirror> <spec>", when that subcommand
    # is implemented
    ls -al "${BUILD_CACHE_DIR}/"
    ls -al "${BUILD_CACHE_DIR}/linux-ubuntu16.04-x86_64/gcc-5.4.0"
else
    echo "spec ${SPEC_NAME} is already up to date on remote mirror"
    # Now that jobs in later stages may depend on this jobs artifacts,
    # we may want to fetch the built tarball from the remote mirror at
    # this point and put it in the artifacts directory.  Or maybe the
    # install command can first look in the artifacts dir, and then on
    # the remote mirror for dependencies?
    spack buildcache download --spec "${SPEC_NAME}" --path "${BUILD_CACHE_DIR}/"
fi
