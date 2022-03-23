#! /usr/bin/env bash

# Copyright 2022 Blue Brain Project 
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


set -e

if [[ $# -ne 1 ]]
then
  echo "Usage: $0 SOURCE_DIR"
  exit -1
fi

SOURCE_DIR="$(realpath $1)"

SPACK_ENV_FILE="${SOURCE_DIR}/spack-build-env.txt"
SPACK_CMAKE_FILE="${SOURCE_DIR}/spack-configure-args.txt"

if [[ ! -f ${SPACK_ENV_FILE} ]]
then
  echo "No such file: ${SPACK_ENV_FILE}"
  exit -1
fi

if [[ ! -f ${SPACK_CMAKE_FILE} ]]
then
  echo "No such file: ${SPACK_CMAKE_FILE}"
  exit -1
fi

prefix=$(grep CMAKE_PREFIX_PATH ${SPACK_ENV_FILE})
prefix=${prefix%%;*}
prefix=${prefix//:/;}
prefix=${prefix/CMAKE_PREFIX_PATH=/CMAKE_PREFIX_PATH=\"}\"

echo " -- The complete CMake command should look something like:"
echo "cmake -DCMAKE_PREFIX_PATH=... FURTHER_FLAGS -B build"
echo ""
echo " -- The CMAKE_PREFIX_PATH should be:"
echo -D$prefix
echo ""
echo " -- Further flags:"
echo $(cat ${SPACK_CMAKE_FILE})
