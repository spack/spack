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

# Get buildcache name so we can write a CDash build id file in the right place
JOB_BUILD_CACHE_ENTRY_NAME=`spack buildcache getname --spec "${SPEC_NAME}"`

if [[ $? -eq 0 ]]; then
    JOB_CDASH_ID_FILE="${BUILD_CACHE_DIR}/${JOB_BUILD_CACHE_ENTRY_NAME}.cdashid"

    # TODO: Build/send POST request to "addBuild" for this job.  Get back the job id and
    # write it to ${JOB_CDASH_ID_FILE}
fi

# Now get CDash ids for dependencies
IFS=';' read -ra DEPS <<< "${DEPENDENCIES}"
for i in "${DEPS[@]}"; do
    echo "Getting cdash id for dependency --> ${i} <--"
    DEP_JOB_BUILDCACHE_NAME=`spack buildcache getname --spec "${i}"`

    if [[ $? -eq 0 ]]; then
        DEP_JOB_ID_FILE="${BUILD_CACHE_DIR}/${DEP_JOB_BUILDCACHE_NAME}.cdashid"

        # TODO: Read dependency CDash id from file named above

        # TODO: Build/send POST request to "relateBuilds" between job and dependency
    fi
done

# Configure mirror
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
    spack install --use-cache "${SPEC_NAME}"

    spack buildcache create -u -a -f -d "${LOCAL_MIRROR}" "${SPEC_NAME}"

    # TODO: Now push buildcache entry to remote mirror, something like:
    # "spack buildcache put <mirror> <spec>", when that subcommand
    # is implemented

    # TODO: Build/send POST request to update CDash job status
else
    echo "spec ${SPEC_NAME} is already up to date on remote mirror"
    # Now that jobs in later stages may depend on this jobs artifacts,
    # we may want to fetch the built tarball from the remote mirror at
    # this point and put it in the artifacts directory.  Or maybe the
    # install command can first look in the artifacts dir, and then on
    # the remote mirror for dependencies?
    spack buildcache download --spec "${SPEC_NAME}" --path "${BUILD_CACHE_DIR}/"

    # TODO: Also here, update CDash job status
fi
