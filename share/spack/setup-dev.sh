#!/bin/sh

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Setup spack
source share/spack/setup-env.sh

# Install git hooks for spack git workflow
cp share/spack/git/hooks/* .git/hooks/

# Add the spack git commands to the path
_spack_pathadd PATH share/spack/git/
