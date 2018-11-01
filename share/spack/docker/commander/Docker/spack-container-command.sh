#!/bin/bash

HOME_DIR=/home/scott

SPACK_COMMAND=""

for i in "${@}"
do
    SPACK_COMMAND="${SPACK_COMMAND} ${i}"
done

cd ${HOME_DIR}/spack

export PATH="${HOME_DIR}/spack/bin:$PATH"

echo "Spack command: ${SPACK_COMMAND}"

SPACK_COMMAND_OUTPUT=$(${SPACK_COMMAND})

echo -e "<BEGIN_SPACK_COMMAND_OUTPUT>\n${SPACK_COMMAND_OUTPUT}\n<END_SPACK_COMMAND_OUTPUT>"
