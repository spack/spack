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
### mirror.  This script also optionally communicates with a remote CDash
### instance to share status on the package build process.
###
### The following environment variables are (possibly) used within this script
### in order for the various elements function properly.
###
### First are two defaults we rely on from gitlab:
###
### CI_PROJECT_DIR
### CI_JOB_NAME
###
### The following must be set up in the variables section of gitlab:
###
### AWS_ACCESS_KEY_ID
### AWS_SECRET_ACCESS_KEY
### SPACK_SIGNING_KEY
###
### SPACK_S3_UPLOAD_MIRROR_URL         // only required in the short term for the cloud case
###
### The following variabes are defined by the ci generation process and are
### required:
###
### SPACK_ENABLE_CDASH
### SPACK_ROOT_SPEC
### SPACK_MIRROR_URL
### SPACK_JOB_SPEC_PKG_NAME
### SPACK_COMPILER_ACTION
###
### Finally, these variables are optionally defined by the ci generation
### process, and may or may not be present:
###
### SPACK_CDASH_BASE_URL
### SPACK_CDASH_PROJECT
### SPACK_CDASH_PROJECT_ENC
### SPACK_CDASH_BUILD_NAME
### SPACK_CDASH_SITE
### SPACK_RELATED_BUILDS
### SPACK_JOB_SPEC_BUILDGROUP
###

shopt -s expand_aliases

export FORCE_UNSAFE_CONFIGURE=1

TEMP_DIR="${CI_PROJECT_DIR}/jobs_scratch_dir"

JOB_LOG_DIR="${TEMP_DIR}/logs"
SPEC_DIR="${TEMP_DIR}/specs"
LOCAL_MIRROR="${CI_PROJECT_DIR}/local_mirror"
BUILD_CACHE_DIR="${LOCAL_MIRROR}/build_cache"
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"

if [ "${SPACK_ENABLE_CDASH}" == "True" ] ; then
    CDASH_UPLOAD_URL="${SPACK_CDASH_BASE_URL}/submit.php?project=${SPACK_CDASH_PROJECT_ENC}"
    DEP_JOB_RELATEBUILDS_URL="${SPACK_CDASH_BASE_URL}/api/v1/relateBuilds.php"
    declare -a JOB_DEPS_PKG_NAMES
fi

export SPACK_ROOT=${CI_PROJECT_DIR}
# export PATH="${SPACK_BIN_DIR}:${PATH}"
export GNUPGHOME="${CI_PROJECT_DIR}/opt/spack/gpg"

. "${CI_PROJECT_DIR}/share/spack/setup-env.sh"

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
    SPEC_YAML_PATH="${SPEC_DIR}/${SPACK_JOB_SPEC_PKG_NAME}.yaml"
    local spec_names_to_save="${SPACK_JOB_SPEC_PKG_NAME}"

    if [ "${SPACK_ENABLE_CDASH}" == "True" ] ; then
        IFS=';' read -ra DEPS <<< "${SPACK_RELATED_BUILDS}"
        for i in "${DEPS[@]}"; do
            depPkgName="${i}"
            spec_names_to_save="${spec_names_to_save} ${depPkgName}"
            JOB_DEPS_PKG_NAMES+=("${depPkgName}")
        done
    fi

    if [ "${SPACK_COMPILER_ACTION}" == "FIND_ANY" ]; then
        # This corresponds to a bootstrapping phase where we need to
        # rely on any available compiler to build the package (i.e. the
        # compiler needed to be stripped from the spec), and thus we need
        # to concretize the root spec again.
        spack -d buildcache save-yaml --specs "${spec_names_to_save}" --root-spec "${SPACK_ROOT_SPEC}" --yaml-dir "${SPEC_DIR}"
    else
        # in this case, either we're relying on Spack to install missing compiler
        # bootstrapped in a previous phase, or else we only had one phase (like a
        # site which already knows what compilers are available on it's runners),
        # so we don't want to concretize that root spec again.  The reason we need
        # this in the first case (bootstrapped compiler), is that we can't concretize
        # a spec at this point if we're going to ask spack to "install_missing_compilers".
        tmp_dir=$(mktemp -d)
        TMP_YAML_PATH="${tmp_dir}/root.yaml"
        ROOT_SPEC_YAML=$(spack python -c "import base64 ; import zlib ; print(str(zlib.decompress(base64.b64decode('${SPACK_ROOT_SPEC}')).decode('utf-8')))")
        echo "${ROOT_SPEC_YAML}" > "${TMP_YAML_PATH}"
        spack -d buildcache save-yaml --specs "${spec_names_to_save}" --root-spec-yaml "${TMP_YAML_PATH}" --yaml-dir "${SPEC_DIR}"
        rm -rf ${tmp_dir}
    fi
}

begin_logging

echo "Running job for spec: ${CI_JOB_NAME}"

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

# To have spack install missing compilers, we need to add a custom
# configuration scope, then we pass that to the package installation
# command
CUSTOM_CONFIG_SCOPE_DIR="${TEMP_DIR}/config_scope"
mkdir -p "${CUSTOM_CONFIG_SCOPE_DIR}"
CUSTOM_CONFIG_SCOPE_ARG=""

if [ "${SPACK_COMPILER_ACTION}" == "INSTALL_MISSING" ]; then
    echo "Make sure bootstrapped compiler will be installed"
    custom_config_file_path="${CUSTOM_CONFIG_SCOPE_DIR}/config.yaml"
      cat <<CONFIG_STUFF > "${custom_config_file_path}"
config:
  install_missing_compilers: true
CONFIG_STUFF
    CUSTOM_CONFIG_SCOPE_ARG="-C ${CUSTOM_CONFIG_SCOPE_DIR}"
    # Configure the binary mirror where, if needed, this jobs compiler
    # was installed in binary pacakge form, then tell spack to
    # install_missing_compilers.
elif [ "${SPACK_COMPILER_ACTION}" == "FIND_ANY" ]; then
    echo "Just find any available compiler"
    spack compiler find
else
    echo "No compiler action to be taken"
fi

# Finally, list the compilers spack knows about
echo "Compiler Configurations:"
spack config get compilers

# Write full-deps yamls for this job spec and its dependencies
gen_full_specs_for_job_and_deps

# Make the build_cache directory if it doesn't exist
mkdir -p "${BUILD_CACHE_DIR}"

# Get buildcache name so we can write a CDash build id file in the right place.
# If we're unable to get the buildcache name, we may have encountered a problem
# concretizing the spec, or some other issue that will eventually cause the job
# to fail.
JOB_BUILD_CACHE_ENTRY_NAME=`spack -d buildcache get-buildcache-name --spec-yaml "${SPEC_YAML_PATH}"`
if [[ $? -ne 0 ]]; then
    echo "ERROR, unable to get buildcache entry name for job ${CI_JOB_NAME}"
    exit 1
fi

if [ "${SPACK_ENABLE_CDASH}" == "True" ] ; then
    # Whether we have to build the spec or download it pre-built, we expect to find
    # the cdash build id file sitting in this location afterwards.
    JOB_CDASH_ID_FILE="${BUILD_CACHE_DIR}/${JOB_BUILD_CACHE_ENTRY_NAME}.cdashid"
fi

# Finally, we can check the spec we have been tasked with build against
# the built binary on the remote mirror to see if it needs to be rebuilt
spack -d buildcache check --spec-yaml "${SPEC_YAML_PATH}" --mirror-url "${SPACK_MIRROR_URL}" --rebuild-on-error

if [[ $? -ne 0 ]]; then
    # Configure mirror
    spack mirror add local_artifact_mirror "file://${LOCAL_MIRROR}"

    if [ "${SPACK_ENABLE_CDASH}" == "True" ] ; then
        JOB_CDASH_ID="NONE"

        # Install package, using the buildcache from the local mirror to
        # satisfy dependencies.
        BUILD_ID_LINE=`spack -d -k -v "${CUSTOM_CONFIG_SCOPE_ARG}" install --keep-stage --cdash-upload-url "${CDASH_UPLOAD_URL}" --cdash-build "${SPACK_CDASH_BUILD_NAME}" --cdash-site "${SPACK_CDASH_SITE}" --cdash-track "${SPACK_JOB_SPEC_BUILDGROUP}" -f "${SPEC_YAML_PATH}" | grep "buildSummary\\.php"`
        check_error $? "spack install"

        # By parsing the output of the "spack install" command, we can get the
        # buildid generated for us by CDash
        JOB_CDASH_ID=$(extract_build_id "${BUILD_ID_LINE}")

        # Write the .cdashid file to the buildcache as well
        echo "${JOB_CDASH_ID}" >> ${JOB_CDASH_ID_FILE}
    else
        spack -d -k -v "${CUSTOM_CONFIG_SCOPE_ARG}" install --keep-stage -f "${SPEC_YAML_PATH}"
    fi

    # Copy some log files into an artifact location, once we have a way
    # to provide a spec.yaml file to more spack commands (e.g. "location")
    # stage_dir=$(spack location --stage-dir -f "${SPEC_YAML_PATH}")
    # build_log_file=$(find -L "${stage_dir}" | grep "spack-build\\.out")
    # config_log_file=$(find -L "${stage_dir}" | grep "config\\.log")
    # cp "${build_log_file}" "${JOB_LOG_DIR}/"
    # cp "${config_log_file}" "${JOB_LOG_DIR}/"

    # Create buildcache entry for this package, reading the spec from the yaml
    # file.
    spack -d buildcache create --spec-yaml "${SPEC_YAML_PATH}" -a -f -d "${LOCAL_MIRROR}" --no-rebuild-index
    check_error $? "spack buildcache create"

    # TODO: The upload-s3 command should eventually be replaced with something
    # like: "spack buildcache put <mirror> <spec>", when that subcommand is
    # properly implemented.
    if [ ! -z "${SPACK_S3_UPLOAD_MIRROR_URL}" ] ; then
        spack -d upload-s3 spec --base-dir "${LOCAL_MIRROR}" --spec-yaml "${SPEC_YAML_PATH}" --endpoint-url "${SPACK_S3_UPLOAD_MIRROR_URL}"
        check_error $? "spack upload-s3 spec"
    else
        spack -d buildcache copy --base-dir "${LOCAL_MIRROR}" --spec-yaml "${SPEC_YAML_PATH}" --destination-url "${SPACK_MIRROR_URL}"
    fi
else
    echo "spec ${CI_JOB_NAME} is already up to date on remote mirror, downloading it"

    # Configure remote mirror so we can download buildcache entry
    spack mirror add remote_binary_mirror ${SPACK_MIRROR_URL}

    # Now download it
    BUILDCACHE_DL_ARGS=("--spec-yaml" "${SPEC_YAML_PATH}" "--path" "${BUILD_CACHE_DIR}/" )
    if [ "${SPACK_ENABLE_CDASH}" == "True" ] ; then
        BUILDCACHE_DL_ARGS+=( "--require-cdashid" )
    fi
    spack -d buildcache download "${BUILDCACHE_DL_ARGS[@]}"
    check_error $? "spack buildcache download"
fi

# The next step is to relate this job to the jobs it depends on
if [ "${SPACK_ENABLE_CDASH}" == "True" ] ; then
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
                    echo "Relating builds -> ${SPACK_CDASH_BUILD_NAME} (buildid=${JOB_CDASH_BUILD_ID}) depends on ${DEP_PKG_NAME} (buildid=${DEP_JOB_CDASH_BUILD_ID})"
                    relateBuildsPostBody="$(get_relate_builds_post_data "${SPACK_CDASH_PROJECT}" ${JOB_CDASH_BUILD_ID} ${DEP_JOB_CDASH_BUILD_ID})"
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
fi

# Show the size of the buildcache and a list of what's in it, directly
# in the gitlab log output
(
    restore_io
    du -sh ${BUILD_CACHE_DIR}
    find ${BUILD_CACHE_DIR} -maxdepth 3 -type d -ls
)

echo "End of rebuild package script"
