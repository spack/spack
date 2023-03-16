# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Universal(CMakePackage):
    """Universal: a header-only C++ template library for universal number arithmetic"""

    homepage = "https://github.com/stillwater-sc/universal"
    url = "https://github.com/stillwater-sc/universal"

    maintainers("eschnett")

    # The release file "3.58b" contains version 3.59.1
    version("3.59.1", sha256="771d64cf51862fdc7c54de585eafac67",
            url="https://github.com/stillwater-sc/universal/archive/refs/tags/v3.58b.tar.gz")
