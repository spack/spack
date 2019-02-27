#!/bin/bash

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

###
### This script represents a gitlab-ci job, corresponding to a single release
### spec.  As such this script must first decide whether or not the spec it
### has been assigned is up to date on the remote binary mirror.  If it is
### not (i.e. the source code has changed in a way that caused a change in the
### full_hash of the spec), this script will build the package, create a
### binary cache for it, and then push all related files to the remote binary
### mirror.  This script also communicates with a remote CDash instance to
### share status on the package build process.
###
### The following environment variables are expected to be set in order for
### the various elements in this script to function properly.  Listed first
### are two defaults we rely on from gitlab, then three we set up in the
### variables section of gitlab ourselves, and finally four variables
### written into the .gitlab-ci.yml file.
###
### CI_PROJECT_DIR
### CI_JOB_NAME
###
### AWS_ACCESS_KEY_ID
### AWS_SECRET_ACCESS_KEY
### SPACK_SIGNING_KEY
###
### CDASH_BASE_URL
### ROOT_SPEC
### DEPENDENCIES
### MIRROR_URL
###

shopt -s expand_aliases

export FORCE_UNSAFE_CONFIGURE=1

TEMP_DIR="${CI_PROJECT_DIR}/jobs_scratch_dir"

JOB_LOG_DIR="${TEMP_DIR}/logs"
SPEC_DIR="${TEMP_DIR}/specs"
LOCAL_MIRROR="${CI_PROJECT_DIR}/local_mirror"
BUILD_CACHE_DIR="${LOCAL_MIRROR}/build_cache"
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
CDASH_UPLOAD_URL="${CDASH_BASE_URL}/submit.php?project=Spack"
DEP_JOB_RELATEBUILDS_URL="${CDASH_BASE_URL}/api/v1/relateBuilds.php"
declare -a JOB_DEPS_PKG_NAMES

export SPACK_ROOT=${CI_PROJECT_DIR}
export PATH="${SPACK_BIN_DIR}:${PATH}"
export GNUPGHOME="${CI_PROJECT_DIR}/opt/spack/gpg"

mkdir -p ${JOB_LOG_DIR}
mkdir -p ${SPEC_DIR}

cleanup() {
    set +x

    if [ -z "$exit_code" ] ; then

        exit_code=$1
        if [ -z "$exit_code" ] ; then
            exit_code=0
        fi

        restore_io

        if [ "$( type -t finalize )" '=' 'function' ] ; then
            finalize "$JOB_LOG_DIR/cdash_log.txt"
        fi

        # We can clean these out later on, once we have a good sense for
        # how the logging infrastructure is working
        # rm -rf "$JOB_LOG_DIR"
    fi

    \exit $exit_code
}

alias exit='cleanup'

begin_logging() {
    trap "cleanup 1; \\exit \$exit_code" INT TERM QUIT
    trap "cleanup 0; \\exit \$exit_code" EXIT

    rm -rf "$JOB_LOG_DIR/cdash_log.txt"

    # NOTE: Here, some redirects are set up
    exec 3>&1 # fd 3 is now a dup of stdout
    exec 4>&2 # fd 4 is now a dup of stderr

    # stdout and stderr are joined and redirected to the log
    exec &> "$JOB_LOG_DIR/cdash_log.txt"

    set -x
}

restore_io() {
    exec  >&-
    exec 2>&-

    exec  >&3
    exec 2>&4

    exec 3>&-
    exec 4>&-
}

finalize() {
    # If you define a finalize function:
    #  - it will always be called at the very end of the script
    #  - the log file will be passed in as the first argument, and
    #  - the code in this function will not be logged.
    echo "The full log file is located at $1"
    # TODO: send this log data to cdash!
}

check_error()
{
    local last_exit_code=$1
    local last_cmd=$2
    if [[ ${last_exit_code} -ne 0 ]]; then
        echo "${last_cmd} exited with code ${last_exit_code}"
        echo "TERMINATING JOB"
        exit 1
    else
        echo "${last_cmd} completed successfully"
    fi
}

extract_build_id()
{
    LINES_TO_SEARCH=$1
    regex="buildSummary\.php\?buildid=([[:digit:]]+)"
    SINGLE_LINE_OUTPUT=$(echo ${LINES_TO_SEARCH} | tr -d '\n')

    if [[ ${SINGLE_LINE_OUTPUT} =~ ${regex} ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        echo "NONE"
    fi
}

get_relate_builds_post_data()
{
  cat <<EOF
{
  "project": "${1}",
  "buildid": ${2},
  "relatedid": ${3},
  "relationship": "depends on"
}
EOF
}

gen_full_specs_for_job_and_deps() {

    read -ra PARTSARRAY <<< "${CI_JOB_NAME}"
    local pkgName="${PARTSARRAY[0]}"
    local pkgVersion="${PARTSARRAY[1]}"
    local compiler="${PARTSARRAY[2]}"
    local osarch="${PARTSARRAY[3]}"

    JOB_SPEC_NAME="${pkgName}@${pkgVersion}%${compiler} arch=${osarch}"
    JOB_PKG_NAME="${pkgName}"
    SPEC_YAML_PATH="${SPEC_DIR}/${pkgName}.yaml"
    local root_spec_name="${ROOT_SPEC}"
    local spec_names_to_save="${pkgName}"

    IFS=';' read -ra DEPS <<< "${DEPENDENCIES}"
    for i in "${DEPS[@]}"; do
        read -ra PARTSARRAY <<< "${i}"
        pkgName="${PARTSARRAY[0]}"
        spec_names_to_save="${spec_names_to_save} ${pkgName}"
        JOB_DEPS_PKG_NAMES+=("${pkgName}")
    done

    spack -d buildcache save-yaml --specs "${spec_names_to_save}" --root-spec "${root_spec_name}" --yaml-dir "${SPEC_DIR}"
}

begin_logging

gen_full_specs_for_job_and_deps

echo "Building package ${JOB_SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

# Finally, list the compilers spack knows about
echo "Compiler Configurations:"
spack config get compilers

# Make the build_cache directory if it doesn't exist
mkdir -p "${BUILD_CACHE_DIR}"

# Get buildcache name so we can write a CDash build id file in the right place.
# If we're unable to get the buildcache name, we may have encountered a problem
# concretizing the spec, or some other issue that will eventually cause the job
# to fail.
JOB_BUILD_CACHE_ENTRY_NAME=`spack -d buildcache get-buildcache-name --spec-yaml "${SPEC_YAML_PATH}"`
if [[ $? -ne 0 ]]; then
    echo "ERROR, unable to get buildcache entry name for job ${CI_JOB_NAME} (spec: ${JOB_SPEC_NAME})"
    exit 1
fi

# This should create the directory we referred to as GNUPGHOME earlier
spack gpg list

# Importing the secret key using gpg2 directly should allow to
# sign and verify both
set +x
KEY_IMPORT_RESULT=`echo ${SPACK_SIGNING_KEY} | base64 --decode | gpg2 --import`
check_error $? "gpg2 --import"
set -x

spack gpg list --trusted
spack gpg list --signing

# Whether we have to build the spec or download it pre-built, we expect to find
# the cdash build id file sitting in this location afterwards.
JOB_CDASH_ID_FILE="${BUILD_CACHE_DIR}/${JOB_BUILD_CACHE_ENTRY_NAME}.cdashid"

# Finally, we can check the spec we have been tasked with build against
# the built binary on the remote mirror to see if it needs to be rebuilt
spack -d buildcache check --spec-yaml "${SPEC_YAML_PATH}" --mirror-url "${MIRROR_URL}" --rebuild-on-error

if [[ $? -ne 0 ]]; then
    # Configure mirror
    spack mirror add local_artifact_mirror "file://${LOCAL_MIRROR}"

    JOB_CDASH_ID="NONE"

    # Install package, using the buildcache from the local mirror to
    # satisfy dependencies.
    BUILD_ID_LINE=`spack -d -k -v install --use-cache --cdash-upload-url "${CDASH_UPLOAD_URL}" --cdash-build "${JOB_SPEC_NAME}" --cdash-site "Spack AWS Gitlab Instance" --cdash-track "Experimental" -f "${SPEC_YAML_PATH}" | grep "buildSummary\\.php"`
    check_error $? "spack install"

    # By parsing the output of the "spack install" command, we can get the
    # buildid generated for us by CDash
    JOB_CDASH_ID=$(extract_build_id "${BUILD_ID_LINE}")

    # Create buildcache entry for this package, reading the spec from the yaml
    # file.
    spack -d buildcache create --spec-yaml "${SPEC_YAML_PATH}" -a -f -d "${LOCAL_MIRROR}" --no-rebuild-index
    check_error $? "spack buildcache create"

    # Write the .cdashid file to the buildcache as well
    echo "${JOB_CDASH_ID}" >> ${JOB_CDASH_ID_FILE}

    # TODO: The upload-s3 command should eventually be replaced with something
    # like: "spack buildcache put <mirror> <spec>", when that subcommand is
    # properly implemented.
    spack -d upload-s3 spec --base-dir "${LOCAL_MIRROR}" --spec-yaml "${SPEC_YAML_PATH}"
    check_error $? "spack upload-s3 spec"
else
    echo "spec ${JOB_SPEC_NAME} is already up to date on remote mirror, downloading it"

    # Configure remote mirror so we can download buildcache entry
    spack mirror add remote_binary_mirror ${MIRROR_URL}

    # Now download it
    spack -d buildcache download --spec-yaml "${SPEC_YAML_PATH}" --path "${BUILD_CACHE_DIR}/" --require-cdashid
    check_error $? "spack buildcache download"
fi

# The next step is to relate this job to the jobs it depends on
if [ -f "${JOB_CDASH_ID_FILE}" ]; then
    JOB_CDASH_BUILD_ID=$(<${JOB_CDASH_ID_FILE})

    if [ "${JOB_CDASH_BUILD_ID}" == "NONE" ]; then
        echo "ERROR: unable to read this jobs id from ${JOB_CDASH_ID_FILE}"
        exit 1
    fi

    # Now get CDash ids for dependencies and "relate" each dependency build
    # with this jobs build
    for DEP_PKG_NAME in "${JOB_DEPS_PKG_NAMES[@]}"; do
        echo "Getting cdash id for dependency --> ${DEP_PKG_NAME} <--"
        DEP_SPEC_YAML_PATH="${SPEC_DIR}/${DEP_PKG_NAME}.yaml"
        DEP_JOB_BUILDCACHE_NAME=`spack -d buildcache get-buildcache-name --spec-yaml "${DEP_SPEC_YAML_PATH}"`

        if [[ $? -eq 0 ]]; then
            DEP_JOB_ID_FILE="${BUILD_CACHE_DIR}/${DEP_JOB_BUILDCACHE_NAME}.cdashid"
            echo "DEP_JOB_ID_FILE path = ${DEP_JOB_ID_FILE}"

            if [ -f "${DEP_JOB_ID_FILE}" ]; then
                DEP_JOB_CDASH_BUILD_ID=$(<${DEP_JOB_ID_FILE})
                echo "File ${DEP_JOB_ID_FILE} contained value ${DEP_JOB_CDASH_BUILD_ID}"
                echo "Relating builds -> ${JOB_SPEC_NAME} (buildid=${JOB_CDASH_BUILD_ID}) depends on ${DEP_PKG_NAME} (buildid=${DEP_JOB_CDASH_BUILD_ID})"
                relateBuildsPostBody="$(get_relate_builds_post_data "Spack" ${JOB_CDASH_BUILD_ID} ${DEP_JOB_CDASH_BUILD_ID})"
                relateBuildsResult=`curl "${DEP_JOB_RELATEBUILDS_URL}" -H "Content-Type: application/json" -H "Accept: application/json" -d "${relateBuildsPostBody}"`
                echo "Result of curl request: ${relateBuildsResult}"
            else
                echo "ERROR: Did not find expected .cdashid file for dependency: ${DEP_JOB_ID_FILE}"
                exit 1
            fi
        else
            echo "ERROR: Unable to get buildcache entry name for ${DEP_SPEC_NAME}"
            exit 1
        fi
    done
else
    echo "ERROR: Did not find expected .cdashid file ${JOB_CDASH_ID_FILE}"
    exit 1
fi

# Show the size of the buildcache and a list of what's in it, directly
# in the gitlab log output
(
    restore_io
    du -sh ${BUILD_CACHE_DIR}
    find ${BUILD_CACHE_DIR} -maxdepth 3 -type d -ls
)

echo "End of rebuild package script"
