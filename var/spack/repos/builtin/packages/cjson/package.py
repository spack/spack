# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Cjson(CMakePackage):
    """Ultralightweight JSON parser in ANSI C."""

    homepage = 'https://github.com/DaveGamble/cJSON'
    git      = 'https://github.com/DaveGamble/cJSON'
    url      = 'https://github.com/DaveGamble/cJSON/archive/refs/tags/v1.7.15.zip'

    version('1.7.15', sha256='c55519316d940757ef93a779f1db1ca809dbf979c551861f339d35aaea1c907c')
