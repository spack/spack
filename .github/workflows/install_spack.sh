#!/usr/bin/env sh
git clone https://github.com/spack/spack.git
echo -e "config:\n  build_jobs: 2" > spack/etc/spack/config.yaml
. spack/share/spack/setup-env.sh
spack compilers
