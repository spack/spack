#!/bin/bash

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

set -x

SPACK_BIN_DIR="${CI_PROJECT_DIR}/bin"
export PATH="${SPACK_BIN_DIR}:${PATH}"

spack upload-s3 index
