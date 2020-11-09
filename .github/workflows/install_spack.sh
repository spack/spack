#!/usr/bin/env sh
. share/spack/setup-env.sh
echo -e "config:\n  build_jobs: 2" > etc/spack/config.yaml
spack config add "packages:all:target:[x86_64]"
# TODO: remove this explicit setting once apple-clang detection is fixed
cat <<EOF > etc/spack/compilers.yaml
compilers:
- compiler:
    spec: apple-clang@11.0.3
    paths:
      cc: /usr/bin/clang
      cxx: /usr/bin/clang++
      f77: /usr/local/bin/gfortran-9
      fc: /usr/local/bin/gfortran-9
    modules: []
    operating_system: catalina
    target: x86_64
EOF
spack compiler info apple-clang
spack debug report
