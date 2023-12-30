#!/bin/bash

# Load spack environment at terminal startup
cat <<EOF >> /root/.bashrc
. /workspaces/spack/share/spack/setup-env.sh
EOF

# Load spack environment in this script
. /workspaces/spack/share/spack/setup-env.sh

# Ensure generic targets for maximum matching with buildcaches
spack config add --scope site "packages:all:require:[target=x86_64_v3]"
spack config add --scope site "concretizer:targets:granularity:generic"

# Setup buildcaches
spack mirror add --scope site develop-root https://binaries.spack.io/develop/root
spack buildcache keys --install --trust
