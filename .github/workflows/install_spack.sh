#!/usr/bin/env sh
. share/spack/setup-env.sh
echo -e "config:\n  build_jobs: 2" > etc/spack/config.yaml
spack config add "packages:all:target:[x86_64]"
spack compiler find
spack compiler info apple-clang
spack debug report
spack solve zlib
