# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Oniguruma(AutotoolsPackage):
    """Regular expression library."""

    homepage = "https://github.com/kkos/oniguruma"
    url      = "https://github.com/kkos/oniguruma/releases/download/v6.1.3/onig-6.1.3.tar.gz"

    version('6.1.3', sha256='480c850cd7c7f2fcaad0942b4a488e2af01fbb8e65375d34908f558b432725cf')
