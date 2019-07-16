#! /usr/bin/env bash

# Remember where we are initially, it's the repo cloned by gitlab-ci
original_directory=$(pwd)
. "${original_directory}/share/spack/setup-env.sh"

# Create a temporary working directory
temp_dir=$(mktemp -d)
trap 'rm -rf "$temp_dir"' INT TERM QUIT EXIT

if [ -z "${DOWNSTREAM_CI_REPO}" ] ; then
    echo "ERROR: missing variable: DOWNSTREAM_CI_REPO" >&2
    exit 1
fi

if [ -z "${SPACK_RELEASE_ENVIRONMENT_PATH}" ] ; then
    echo "ERROR: missing variable: SPACK_RELEASE_ENVIRONMENT_PATH" >&2
    exit 1
fi

if [ -z "${CDASH_AUTH_TOKEN}" ] ; then
    echo "WARNING: missing variable: CDASH_AUTH_TOKEN" >&2
else
    token_file="${temp_dir}/cdash_auth_token"
    echo ${CDASH_AUTH_TOKEN} > ${token_file}
fi

if [ -z "${SPACK_RELEASE_ENVIRONMENT_REPO}" ] ; then
    echo "Assuming spack repo contains environment" >&2
    env_repo_dir=${original_directory}
else
    echo "Cloning ${SPACK_RELEASE_ENVIRONMENT_REPO} into ${temp_dir}/envrepo" >&2
    cd ${temp_dir}
    git clone ${SPACK_RELEASE_ENVIRONMENT_REPO} envrepo
    cd envrepo
    env_repo_dir=$(pwd)
fi

current_branch="$CI_COMMIT_REF_NAME"

# Because want to see generated gitlab-ci file as an artifact,
# we need to write it within the spack repo cloned by gitlab-ci.
gen_ci_dir="${original_directory}/ci-generation"
gen_ci_file="${gen_ci_dir}/.gitlab-ci.yml"
mkdir -p ${gen_ci_dir}

env_dir="${env_repo_dir}/${SPACK_RELEASE_ENVIRONMENT_PATH}"

if [ ! -f "${env_dir}/spack.yaml" ] ; then
    echo "ERROR: Cannot find spack environment file in ${env_dir}"
    exit 1
fi

cd $env_dir

# The next commands generates the .gitlab-ci.yml (and optionally creates a
# buildgroup in cdash)
RELEASE_JOBS_ARGS=("--output-file" "${gen_ci_file}")
if [ ! -z "${token_file}" ]; then
    RELEASE_JOBS_ARGS+=("--cdash-credentials" "${token_file}")
fi

spack release-jobs "${RELEASE_JOBS_ARGS[@]}"

if [[ $? -ne 0 ]]; then
    echo "spack release-jobs command failed"
    exit 1
fi

cp ${gen_ci_file} "${original_directory}/.gitlab-ci.yml"

# Remove global from here, it's clobbering people git identity config
git config --global user.email "robot@spack.io"
git config --global user.name "Build Robot"

commit_msg="Auto-generated commit testing ${current_branch} (${CI_COMMIT_SHA})"

cd ${original_directory}
echo "git status"
git status
echo "git branch"
git branch -D ___multi_ci___ 2> /dev/null || true
echo "git checkout"
git checkout -b ___multi_ci___
echo "git add"
git add .gitlab-ci.yml
echo "git commit"
git commit -m "$commit_msg"
echo "git commit-tree/reset"
# Prepare to send the whole working copy.  Doing this instead should be faster
# until we decide to come up with a way of automatically keeping the downstream
# repo in sync with the main one, at which point just pushing a single, new
# commit with the change would be faster.
git reset "$( git commit-tree HEAD^{tree} -m ${commit_msg} )"
echo "git status"
git status
echo "git push"
git push --force "$DOWNSTREAM_CI_REPO" \
    "___multi_ci___:multi-ci-${current_branch}"
