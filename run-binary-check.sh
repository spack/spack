#!/bin/bash

set -ex

uname -a
pwd
ls -al
git --version
python --version

SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"

which spack
spack --version

git branch -a

spack checkbinaries --base origin/develop --mirror_url http://172.17.0.1:8081/
