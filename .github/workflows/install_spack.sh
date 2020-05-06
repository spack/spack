#!/usr/bin/env sh
git clone https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
spack compilers
