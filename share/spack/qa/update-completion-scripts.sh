#!/usr/bin/env bash
#
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Updates Spack's shell tab completion scripts

# Switch to parent directory
QA_DIR="$(dirname "${BASH_SOURCE[0]}")"
cd "$QA_DIR/.."

# Update each shell
for shell in bash # zsh fish
do
    header=$shell/spack-completion.in
    script=spack-completion.$shell

    rm -f $script
    spack commands --aliases --format=$shell --header=$header --update=$script
    chmod +x $script
done
