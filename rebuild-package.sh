#!/bin/bash

set -x

export FORCE_UNSAFE_CONFIGURE=1

build_spec_name() {
    read -ra PARTSARRAY <<< "$1"
    pkgName="${PARTSARRAY[0]}"
    pkgVersion="${PARTSARRAY[1]}"
    compiler="${PARTSARRAY[2]}"
    osarch="${PARTSARRAY[3]}"

    echo "${pkgName}@${pkgVersion}%${compiler} arch=${osarch}"
}

SPEC_NAME=$( build_spec_name "${CI_JOB_NAME}" )
echo "Building package ${SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

CURRENT_WORKING_DIR=`pwd`
LOCAL_MIRROR="${CURRENT_WORKING_DIR}/local_mirror"
BUILD_CACHE_DIR="${LOCAL_MIRROR}/build_cache"
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"
export GNUPGHOME="${CURRENT_WORKING_DIR}/opt/spack/gpg"

# If we have been given a list of paths where we might find compilers
if [ ! -z "${SPACK_FIND_COMPILER_PATHS}" ]; then
    IFS=';' read -ra COMPILER_PATHS <<< "${SPACK_FIND_COMPILER_PATHS}"
    for path in "${COMPILER_PATHS[@]}"; do
        echo "Finding compiler in ${path}"
        if [ -d "${path}" ]; then
            spack compiler find "${path}"
        fi
    done

    # Finally, list the compilers spack knows about
    spack compilers
fi

# Make the build_cache directory if it doesn't exist
mkdir -p "${BUILD_CACHE_DIR}"

# Get buildcache name so we can write a CDash build id file in the right place.
# If we're unable to get the buildcache name, we may have encountered a problem
# concretizing the spec, or some other issue that will eventually cause the job
# to fail.
JOB_BUILD_CACHE_ENTRY_NAME=`spack buildcache get-name --spec "${SPEC_NAME}"`
if [[ $? -ne 0 ]]; then
    echo "ERROR, unable to get buildcache entry name for job ${CI_JOB_NAME} (spec: ${SPEC_NAME})"
    exit 1
fi

# This should create the directory we referred to as GNUPGHOME earlier
spack gpg list

# Importing the secret key using gpg2 directly should allow to
# sign and verify both
echo ${SPACK_SIGNING_KEY} | base64 --decode | gpg2 --import

# This line doesn't seem to add any extra trust levels
# echo ${SPACK_SIGNING_KEY} | base64 --decode | spack gpg trust /dev/stdin

spack gpg list --trusted
spack gpg list --signing

JOB_CDASH_ID="NONE"

# Finally, we can check the spec we have been tasked with build against
# the built binary on the remote mirror to see if it needs to be rebuilt
spack buildcache check --spec "${SPEC_NAME}" --mirror-url "${MIRROR_URL}" --no-index

if [[ $? -ne 0 ]]; then
    # Configure mirror
    spack mirror add local_artifact_mirror "file://${LOCAL_MIRROR}"

    CDASH_UPLOAD_URL="${CDASH_BASE_URL}/submit.php?project=Spack"

    # Install package, using the buildcache from the local mirror to
    # satisfy dependencies.
    INSTALL_OUTPUT=$(spack -d install --use-cache --cdash-upload-url "${CDASH_UPLOAD_URL}" --cdash-build "${SPEC_NAME}" --cdash-site "Spack AWS Gitlab Instance" --cdash-track "Experimental" "${SPEC_NAME}")

    # By parsing the output of the "spack install" command, we can get the
    # buildid generated for us by CDash

    # Create buildcache entry for this package
    spack buildcache create -a -f -d "${LOCAL_MIRROR}" "${SPEC_NAME}"

    # TODO: Now push buildcache entry to remote mirror, something like:
    # "spack buildcache put <mirror> <spec>", when that subcommand
    # is implemented
    spack upload-s3 spec --base-dir "${LOCAL_MIRROR}" --spec "${SPEC_NAME}"
else
    echo "spec ${SPEC_NAME} is already up to date on remote mirror, downloading it"

    # Configure remote mirror so we can download buildcache entry
    spack mirror add remote_binary_mirror ${MIRROR_URL}

    # Now download it
    spack buildcache download --spec "${SPEC_NAME}" --path "${BUILD_CACHE_DIR}/"
fi

# Now, whether we had to build the spec or download it pre-built, we should have
# the cdash build id handy as well.  We use it to link this job to the jobs it
# depends on in CDash.
if [ "${JOB_CDASH_ID}" != "NONE" ]; then
    JOB_CDASH_ID_FILE="${BUILD_CACHE_DIR}/${JOB_BUILD_CACHE_ENTRY_NAME}.cdashid"

    if [ ! -f "${}" ]; then
        echo "ERROR: Did not find expected .cdashid file ${JOB_CDASH_ID_FILE}"
        exit 1
    fi

    # JOB_CDASH_BUILD_ID=""

    # Now get CDash ids for dependencies
    IFS=';' read -ra DEPS <<< "${DEPENDENCIES}"
    for i in "${DEPS[@]}"; do
        echo "Getting cdash id for dependency --> ${i} <--"
        DEP_SPEC_NAME=$( build_spec_name "${i}" )
        DEP_JOB_BUILDCACHE_NAME=`spack buildcache get-name --spec "${DEP_SPEC_NAME}"`

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
fi
