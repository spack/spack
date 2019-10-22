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

cd "$original_directory"
mv .git "$temp_dir/original-git-dir"
git init .

git config user.email "robot@spack.io"
git config user.name "Spack Build Bot"

cp ${gen_ci_file} "${original_directory}/.gitlab-ci.yml"
git add .

echo "git commit"
commit_message="Auto-generated commit testing"
commit_message="${commit_message} ${current_branch} (${CI_COMMIT_SHA})"
git commit --message="${commit_message}"

echo "git push"
git remote add origin "$DOWNSTREAM_CI_REPO"
git push --force origin "master:multi-ci-${current_branch}"

rm -rf .git
mv "$temp_dir/original-git-dir" .git
git reset --hard HEAD
