#! /usr/bin/env bash

if [ -z "$DOWNSTREAM_CI_REPO" ] ; then
    echo "Warning: missing variable: DOWNSTREAM_CI_REPO" >&2
fi

current_branch="$CI_COMMIT_REF_NAME"

original_directory=$(pwd)
workdir="${original_directory}/ci-generation"
mkdir -p ${workdir}
cd $workdir

micro_service_url="https://internal.spack.io/glciy/${CI_COMMIT_SHA}.yaml"
wget ${micro_service_url}
yaml_file="${workdir}/${CI_COMMIT_SHA}.yaml"
cp "$yaml_file" "${original_directory}/.gitlab-ci.yml"

py_script="${original_directory}/bin/create-buildgroups.py"
$py_script --credentials ${CDASH_AUTH_TOKEN} \
           --buildfile ${yaml_file} \
           --projectid "2" \
           --siteid "3" \
           --cdash-url "https://cdash.spack.io"

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
git reset "$( git commit-tree HEAD^{tree} -m ${commit_msg} )"
echo "git status"
git status
echo "git push"
git push --force "$DOWNSTREAM_CI_REPO" \
    "___multi_ci___:$current_branch"
