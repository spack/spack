#!/bin/bash

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

export FORCE_UNSAFE_CONFIGURE=1

# TEMP_DIR="$( mktemp -d )"
TEMP_DIR="${CI_PROJECT_DIR}/jobs_scratch_dir"

JOB_LOG_DIR="${TEMP_DIR}/logs"
SPEC_DIR="${TEMP_DIR}/specs"
CURRENT_WORKING_DIR=`pwd`
LOCAL_MIRROR="${CURRENT_WORKING_DIR}/local_mirror"
BUILD_CACHE_DIR="${LOCAL_MIRROR}/build_cache"
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
CDASH_UPLOAD_URL="${CDASH_BASE_URL}/submit.php?project=Spack"
DEP_JOB_RELATEBUILDS_URL="${CDASH_BASE_URL}/api/v1/relateBuilds.php"
declare -a JOB_DEPS_PKG_NAMES

export SPACK_ROOT=${CI_PROJECT_DIR}
export PATH="${SPACK_BIN_DIR}:${PATH}"
export GNUPGHOME="${CURRENT_WORKING_DIR}/opt/spack/gpg"

mkdir -p ${JOB_LOG_DIR}
mkdir -p ${SPEC_DIR}

cleanup() {
    set +x

    if [ -z "$exit_code" ] ; then

        exit_code=$1
        if [ -z "$exit_code" ] ; then
            exit_code=0
        fi

        [ -n "$stdout_pid" ] && kill "$stdout_pid" ; unset stdout_pid
        [ -n "$stderr_pid" ] && kill "$stderr_pid" ; unset stderr_pid
        [ -n "$log_pid"    ] && kill "$log_pid"    ; unset log_pid

        wait

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

begin_logging() {
    trap "cleanup 1; \\exit \$exit_code" INT TERM QUIT
    trap "cleanup 0; \\exit \$exit_code" EXIT

    rm -rf "$JOB_LOG_DIR/cdash_log.txt"

    mkfifo "$JOB_LOG_DIR/stdout"
    mkfifo "$JOB_LOG_DIR/stderr"

    (
        stdbuf -o0 cat "$JOB_LOG_DIR/stdout" |
        stdbuf -i0 -o0 sed -s 's/^/STDOUT: /g' >> "$JOB_LOG_DIR/cdash_log.txt"
    ) &
    stdout_pid="$!"

    (
        stdbuf -o0 cat "$JOB_LOG_DIR/stderr" |
        stdbuf -i0 -o0 sed -s 's/^/STDERR: /g' >> "$JOB_LOG_DIR/cdash_log.txt"
    ) &
    stderr_pid="$!"

    # NOTE: Here, some redirects are set up
    exec 3>&1 # fd 3 is now a dup of stdout
    exec 4>&2 # fd 4 is now a dup of stderr

    # fd 1 (formerly stdout) now goes to the named pipe set aside for
    # redirecting stdout
    exec  >"$JOB_LOG_DIR/stdout"

    # fd 2 (formerly stderr) now goes to the named pipe set aside for
    # redirecting stderr
    exec 2>"$JOB_LOG_DIR/stderr"

    # The named pipes are unlinked (*not* removed).
    # Since all opened operations are complete, we don't need to actually keep
    # them visible on the file system.  The OS will garbage collect their inodes
    # once the last fd pointing to them is closed.
    #
    # BTW, this is, more-or-less, how python implements os.pipe() on linux
    unlink "$JOB_LOG_DIR/stdout"
    unlink "$JOB_LOG_DIR/stderr"

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

# gen_full_spec() {
#     yaml_path=$1

#     read -ra PARTSARRAY <<< "$2"
#     pkgName="${PARTSARRAY[0]}"
#     pkgVersion="${PARTSARRAY[1]}"
#     compiler="${PARTSARRAY[2]}"
#     osarch="${PARTSARRAY[3]}"

#     dep_spec_name="${pkgName}@${pkgVersion}%${compiler} arch=${osarch}"
#     root_spec_name="${ROOT_SPEC} arch=${osarch}"

#     spack buildcache save-yaml --spec "${pkgName}" --root-spec "${root_spec_name}" --yaml-path "${yaml_path}"

#     echo "${pkgName}@${pkgVersion}%${compiler} arch=${osarch}"
# }

gen_full_specs_for_job_and_deps() {

    read -ra PARTSARRAY <<< "${CI_JOB_NAME}"
    local pkgName="${PARTSARRAY[0]}"
    local pkgVersion="${PARTSARRAY[1]}"
    local compiler="${PARTSARRAY[2]}"
    local osarch="${PARTSARRAY[3]}"

    JOB_SPEC_NAME="${pkgName}@${pkgVersion}%${compiler} arch=${osarch}"
    JOB_PKG_NAME="${pkgName}"
    SPEC_YAML_PATH="${SPEC_DIR}/${pkgName}.yaml"
    local root_spec_name="${ROOT_SPEC} arch=${osarch}"
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

# SPEC_YAML_PATH="${SPEC_DIR}/spec.yaml"
# JOB_SPEC_NAME=$( gen_full_spec "${SPEC_YAML_PATH}" "${CI_JOB_NAME}" )

gen_full_specs_for_job_and_deps

echo "Building package ${JOB_SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

# echo "Saved full spec yaml to ${SPEC_YAML_PATH}"
# echo "Saved full spec yaml to ${SPEC_YAML_PATH}, contents:"
# cat ${SPEC_YAML_PATH}

# Finally, list the compilers spack knows about
spack compilers

# Show the compiler details
echo "Compiler Configurations:"
cat ~/.spack/linux/compilers.yaml

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

# This line doesn't seem to add any extra trust levels
# echo ${SPACK_SIGNING_KEY} | base64 --decode | spack gpg trust /dev/stdin

spack gpg list --trusted
spack gpg list --signing

# Finally, we can check the spec we have been tasked with build against
# the built binary on the remote mirror to see if it needs to be rebuilt
spack -d buildcache check --spec-yaml "${SPEC_YAML_PATH}" --mirror-url "${MIRROR_URL}" --no-index

if [[ $? -ne 0 ]]; then
    # Configure mirror
    spack mirror add local_artifact_mirror "file://${LOCAL_MIRROR}"

    JOB_CDASH_ID="NONE"

    # Install package, using the buildcache from the local mirror to
    # satisfy dependencies.
    BUILD_ID_LINE=`spack -d -k install --use-cache --cdash-upload-url "${CDASH_UPLOAD_URL}" --cdash-build "${JOB_SPEC_NAME}" --cdash-site "Spack AWS Gitlab Instance" --cdash-track "Experimental" -f "${SPEC_YAML_PATH}" | grep "buildSummary\\.php"`
    check_error $? "spack install"

    # By parsing the output of the "spack install" command, we can get the
    # buildid generated for us by CDash
    JOB_CDASH_ID=$(extract_build_id "${BUILD_ID_LINE}")

    BUILD_ID_ARG=""
    if [ "${JOB_CDASH_ID}" != "NONE" ]; then
        echo "Found build id for ${JOB_SPEC_NAME} from 'spack install' output: ${JOB_CDASH_ID}"
        BUILD_ID_ARG="--cdash-build-id \"${JOB_CDASH_ID}\""
    else
        echo "Unable to find build id in install output, install probably failed."
        exit 1
    fi

    # Create buildcache entry for this package.  We should eventually change
    # this to read the spec from the yaml file, but it seems unlikely there
    # will be a spec that matches the name which is NOT the same as represented
    # in the yaml file
    spack -d buildcache create --spec-yaml "${SPEC_YAML_PATH}" -a -f -d "${LOCAL_MIRROR}" ${BUILD_ID_ARG}
    check_error $? "spack buildcache create"

    # TODO: Now push buildcache entry to remote mirror, something like:
    # "spack buildcache put <mirror> <spec>", when that subcommand
    # is implemented
    spack -d upload-s3 spec --base-dir "${LOCAL_MIRROR}" --spec-yaml "${SPEC_YAML_PATH}"
    check_error $? "spack upload-s3 spec"
else
    echo "spec ${JOB_SPEC_NAME} is already up to date on remote mirror, downloading it"

    # Configure remote mirror so we can download buildcache entry
    spack mirror add remote_binary_mirror ${MIRROR_URL}

    # Now download it
    spack -d buildcache download --spec-yaml "${SPEC_YAML_PATH}" --path "${BUILD_CACHE_DIR}/"
    check_error $? "spack buildcache download"
fi

# Now, whether we had to build the spec or download it pre-built, we should have
# the cdash build id file sitting in place as well.  We use it to link this job to
# the jobs it depends on in CDash.
JOB_CDASH_ID_FILE="${BUILD_CACHE_DIR}/${JOB_BUILD_CACHE_ENTRY_NAME}.cdashid"

if [ -f "${JOB_CDASH_ID_FILE}" ]; then
    JOB_CDASH_BUILD_ID=$(<${JOB_CDASH_ID_FILE})

    if [ "${JOB_CDASH_BUILD_ID}" == "NONE" ]; then
        echo "ERROR: unable to read this jobs id from ${JOB_CDASH_ID_FILE}"
        exit 1
    fi

    # Now get CDash ids for dependencies and "relate" each dependency build
    # with this jobs build
    # IFS=';' read -ra DEPS <<< "${DEPENDENCIES}"
    # for i in "${DEPS[@]}"; do
    for DEP_PKG_NAME in "${JOB_DEPS_PKG_NAMES[@]}"; do
        echo "Getting cdash id for dependency --> ${i} <--"
        # DEP_SPEC_YAML_DIR=$(mktemp -d)
        DEP_SPEC_YAML_PATH="${SPEC_DIR}/${DEP_PKG_NAME}.yaml"
        # DEP_SPEC_NAME=$( gen_full_spec "${DEP_SPEC_YAML_PATH}" "${i}" )
        # echo "dependency spec name = ${DEP_SPEC_NAME}"
        # echo "dependency spec name = ${DEP_SPEC_NAME}, spec yaml saved to ${DEP_SPEC_YAML_PATH}"
        echo "dependency spec name = ${DEP_PKG_NAME}, spec yaml saved to ${DEP_SPEC_YAML_PATH}"
        # echo "dependency spec yaml contents:"
        # cat ${DEP_SPEC_YAML_PATH}
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

echo "This line should be logged"
