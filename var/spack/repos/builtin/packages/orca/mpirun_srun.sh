#!/bin/sh
# Replacement wrapper for mpirun when only srun is available

srun $(echo "${@}" | sed 's/-np/-n/')
