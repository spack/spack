#!/bin/bash
set -ex
source share/spack/setup-env.sh
$PYTHON bin/spack bootstrap disable spack-install
$PYTHON bin/spack -d solve zlib
tree $BOOTSTRAP/store
exit 0
