# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Oniguruma(AutotoolsPackage):
    """Regular expression library."""

    homepage = "https://github.com/kkos/oniguruma"
    url      = "https://github.com/kkos/oniguruma/releases/download/v6.1.3/onig-6.1.3.tar.gz"

    version('6.1.3', '2d105d352c3f852d662414f639e7e859')
