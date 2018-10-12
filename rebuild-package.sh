#!/bin/bash

set -x

export FORCE_UNSAFE_CONFIGURE=1

echo "Building package ${SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

CURRENT_WORKING_DIR=`pwd`
LOCAL_MIRROR="${CURRENT_WORKING_DIR}/local_mirror"
BUILD_CACHE_DIR="${LOCAL_MIRROR}/build_cache"
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"
export GNUPGHOME="${CURRENT_WORKING_DIR}/opt/spack/gpg"

# Make the build_cache directory if it doesn't exist
mkdir -p "${BUILD_CACHE_DIR}"

# Get buildcache name so we can write a CDash build id file in the right place
JOB_BUILD_CACHE_ENTRY_NAME=`spack buildcache get-name --spec "${SPEC_NAME}"`

if [[ $? -eq 0 ]]; then
    JOB_CDASH_ID_FILE="${BUILD_CACHE_DIR}/${JOB_BUILD_CACHE_ENTRY_NAME}.cdashid"
    JOB_ADDBUILD_URL="${CDASH_BASE_URL}/api/v1/addBuild.php"

    # TODO: Build/send POST request to "addBuild" for this job.  Get back the job id and
    # write it to ${JOB_CDASH_ID_FILE}.

    # Required params:
    #   project = based on release
    #   site = ?
    #   name = derived from job name
    #   stamp = e.g. "20180911-0136-Experimental"

fi

# Now get CDash ids for dependencies
IFS=';' read -ra DEPS <<< "${DEPENDENCIES}"
for i in "${DEPS[@]}"; do
    echo "Getting cdash id for dependency --> ${i} <--"
    DEP_JOB_BUILDCACHE_NAME=`spack buildcache get-name --spec "${i}"`

    if [[ $? -eq 0 ]]; then
        DEP_JOB_ID_FILE="${BUILD_CACHE_DIR}/${DEP_JOB_BUILDCACHE_NAME}.cdashid"
        DEP_JOB_RELATEBUILDS_URL="${CDASH_BASE_URL}/api/v1/relateBuilds.php"
        # TODO: Read dependency CDash id from file named above

        # TODO: Build/send POST request to "relateBuilds" between job and dependency,
        # Required params:
        #   buildid = this build's id
        #   relatedid = dependency's buildid
        #   relationship = "depends on"
    fi
done

# This should create the directory we referred to as GNUPGHOME earlier
spack gpg list

# Importing the secret key using gpg2 directly should allow to
# sign and verify both
echo ${SPACK_SIGNING_KEY} | base64 --decode | gpg2 --import

# This line doesn't seem to add any extra trust levels
# echo ${SPACK_SIGNING_KEY} | base64 --decode | spack gpg trust /dev/stdin

spack gpg list --trusted
spack gpg list --signing


# Finally, we can check the spec we have been tasked with build against
# the built binary on the remote mirror to see if it needs to be rebuilt
spack -d buildcache check --spec "${SPEC_NAME}" --mirror-url "${MIRROR_URL}" --no-index

if [[ $? -ne 0 ]]; then
    # Configure mirror
    spack mirror add local_artifact_mirror "file://${LOCAL_MIRROR}"

    # Install package, using the buildcache from the local mirror to
    # satisfy dependencies.
    spack -d install --use-cache "${SPEC_NAME}"

    # Create buildcache entry for this package
    spack -d buildcache create -a -f -d "${LOCAL_MIRROR}" "${SPEC_NAME}"

    # TODO: Now push buildcache entry to remote mirror, something like:
    # "spack buildcache put <mirror> <spec>", when that subcommand
    # is implemented
    spack upload-s3 spec --base-dir "${LOCAL_MIRROR}" --spec "${SPEC_NAME}"

    # TODO: Build/send POST request to update CDash job status
else
    echo "spec ${SPEC_NAME} is already up to date on remote mirror, downloading it"

    # Configure remote mirror so we can download buildcache entry
    spack mirror add remote_binary_mirror ${MIRROR_URL}

    # Now download it
    spack buildcache download --spec "${SPEC_NAME}" --path "${BUILD_CACHE_DIR}/"

    # TODO: Also here, update CDash job status
fi
