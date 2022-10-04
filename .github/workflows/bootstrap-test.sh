#!/bin/bash
set -ex
source share/spack/setup-env.sh
$PYTHON bin/spack bootstrap untrust spack-install
$PYTHON bin/spack -d solve zlib
tree $BOOTSTRAP/store
exit 0
