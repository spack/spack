#!/bin/bash

export FORCE_UNSAFE_CONFIGURE=1

check_error()
{
    if [[ $? -ne 0 ]]; then
        exit 1
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

gen_full_spec() {
    yaml_path=$1

    read -ra PARTSARRAY <<< "$2"
    pkgName="${PARTSARRAY[0]}"
    pkgVersion="${PARTSARRAY[1]}"
    compiler="${PARTSARRAY[2]}"
    osarch="${PARTSARRAY[3]}"

    dep_spec_name="${pkgName}@${pkgVersion}%${compiler} arch=${osarch}"
    root_spec_name="${ROOT_SPEC} arch=${osarch}"

    spack buildcache save-yaml --spec "${pkgName}" --root-spec "${root_spec_name}" --yaml-path "${yaml_path}"

    echo "${pkgName}@${pkgVersion}%${compiler} arch=${osarch}"
}

CURRENT_WORKING_DIR=`pwd`
LOCAL_MIRROR="${CURRENT_WORKING_DIR}/local_mirror"
BUILD_CACHE_DIR="${LOCAL_MIRROR}/build_cache"
SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
CDASH_UPLOAD_URL="${CDASH_BASE_URL}/submit.php?project=Spack"
DEP_JOB_RELATEBUILDS_URL="${CDASH_BASE_URL}/api/v1/relateBuilds.php"

export SPACK_ROOT=${CI_PROJECT_DIR}
export PATH="${SPACK_BIN_DIR}:${PATH}"
export GNUPGHOME="${CURRENT_WORKING_DIR}/opt/spack/gpg"

SPEC_DIR=$(mktemp -d)
SPEC_YAML_PATH="${SPEC_DIR}/spec.yaml"

SPEC_NAME=$( gen_full_spec "${SPEC_YAML_PATH}" "${CI_JOB_NAME}" )
echo "Building package ${SPEC_NAME}, ${HASH}, ${MIRROR_URL}"

echo "Saved full spec yaml to ${SPEC_YAML_PATH}, contents:"
cat ${SPEC_YAML_PATH}

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
JOB_BUILD_CACHE_ENTRY_NAME=`spack buildcache get-buildcache-name --spec-yaml "${SPEC_YAML_PATH}"`
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

# Finally, we can check the spec we have been tasked with build against
# the built binary on the remote mirror to see if it needs to be rebuilt
spack -d buildcache check --spec-yaml "${SPEC_YAML_PATH}" --mirror-url "${MIRROR_URL}" --no-index

if [[ $? -ne 0 ]]; then
    # Configure mirror
    spack mirror add local_artifact_mirror "file://${LOCAL_MIRROR}"

    JOB_CDASH_ID="NONE"

    # Install package, using the buildcache from the local mirror to
    # satisfy dependencies.
    INSTALL_OUTPUT=$(spack -d install --use-cache --cdash-upload-url "${CDASH_UPLOAD_URL}" --cdash-build "${SPEC_NAME}" --cdash-site "Spack AWS Gitlab Instance" --cdash-track "Experimental" -f "${SPEC_YAML_PATH}")
    check_error $?
    echo -e "spack install output:\n${INSTALL_OUTPUT}"

    # By parsing the output of the "spack install" command, we can get the
    # buildid generated for us by CDash
    JOB_CDASH_ID=$(extract_build_id "${INSTALL_OUTPUT}")

    BUILD_ID_ARG=""
    if [ "${JOB_CDASH_ID}" != "NONE" ]; then
        echo "Found build id for ${SPEC_NAME} from 'spack install' output: ${JOB_CDASH_ID}"
        BUILD_ID_ARG="--cdash-build-id \"${JOB_CDASH_ID}\""
    fi

    # Create buildcache entry for this package.  We should eventually change
    # this to read the spec from the yaml file, but it seems unlikely there
    # will be a spec that matches the name which is NOT the same as represented
    # in the yaml file
    BUILDCACHE_CREATE_OUTPUT=$(spack -d buildcache create --spec-yaml "${SPEC_YAML_PATH}" -a -f -d "${LOCAL_MIRROR}" ${BUILD_ID_ARG})
    check_error $?
    echo -e "spack buildcache create output:\n${BUILDCACHE_CREATE_OUTPUT}"

    # TODO: Now push buildcache entry to remote mirror, something like:
    # "spack buildcache put <mirror> <spec>", when that subcommand
    # is implemented
    spack upload-s3 spec --base-dir "${LOCAL_MIRROR}" --spec-yaml "${SPEC_YAML_PATH}"
    check_error $?
else
    echo "spec ${SPEC_NAME} is already up to date on remote mirror, downloading it"

    # Configure remote mirror so we can download buildcache entry
    spack mirror add remote_binary_mirror ${MIRROR_URL}

    # Now download it
    spack buildcache download --spec-yaml "${SPEC_YAML_PATH}" --path "${BUILD_CACHE_DIR}/"
    check_error $?
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
    IFS=';' read -ra DEPS <<< "${DEPENDENCIES}"
    for i in "${DEPS[@]}"; do
        echo "Getting cdash id for dependency --> ${i} <--"
        DEP_SPEC_YAML_DIR=$(mktemp -d)
        DEP_SPEC_YAML_PATH="${DEP_SPEC_YAML_DIR}/spec.yaml"
        DEP_SPEC_NAME=$( gen_full_spec "${DEP_SPEC_YAML_PATH}" "${i}" )
        echo "dependency spec name = ${DEP_SPEC_NAME}"
        echo "dependency spec yaml contents:"
        cat ${DEP_SPEC_YAML_PATH}
        DEP_JOB_BUILDCACHE_NAME=`spack buildcache get-buildcache-name --spec-yaml "${DEP_SPEC_YAML_PATH}"`

        if [[ $? -eq 0 ]]; then
            DEP_JOB_ID_FILE="${BUILD_CACHE_DIR}/${DEP_JOB_BUILDCACHE_NAME}.cdashid"
            echo "DEP_JOB_ID_FILE path = ${DEP_JOB_ID_FILE}"

            if [ -f "${DEP_JOB_ID_FILE}" ]; then
                DEP_JOB_CDASH_BUILD_ID=$(<${DEP_JOB_ID_FILE})
                echo "File ${DEP_JOB_ID_FILE} contained value ${DEP_JOB_CDASH_BUILD_ID}"
                echo "Relating builds -> ${SPEC_NAME} (buildid=${JOB_CDASH_BUILD_ID}) depends on ${DEP_SPEC_NAME} (buildid=${DEP_JOB_CDASH_BUILD_ID})"
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

# Show the size of the buildcache and a list of what's in it
set -x
du -sh ${BUILD_CACHE_DIR}
find ${BUILD_CACHE_DIR} -maxdepth 3 -type d -ls
