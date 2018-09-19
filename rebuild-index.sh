#!/bin/bash

set -x

SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"

spack upload-s3 index
