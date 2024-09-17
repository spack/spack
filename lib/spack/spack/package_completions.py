# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Functions relating to shell autocompletion scripts for packages.
"""

from spack.package_base import PackageBase


def bash_completion_path(pkg: PackageBase) -> str:
    return f"{pkg.prefix}/share/bash-completion/completions"


def zsh_completion_path(pkg: PackageBase) -> str:
    return f"{pkg.prefix}/share/zsh/site-functions"


def fish_completion_path(pkg: PackageBase) -> str:
    return f"{pkg.prefix}/share/fish/vendor_completions.d"
