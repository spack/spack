# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RGbrd(RPackage):
    """Utilities for processing Rd objects and files.

    Provides utilities for processing Rd objects and files. Extract argument
    descriptions and other parts of the help pages of functions."""

    cran = "gbRd"

    version('0.4-11', sha256='0251f6dd6ca987a74acc4765838b858f1edb08b71dbad9e563669b58783ea91b')
