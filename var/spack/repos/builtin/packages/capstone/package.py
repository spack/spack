# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Capstone(CMakePackage):
    """Capstone is a lightweight multi-platform,
       multi-architecture disassembly framework."""

    homepage = "http://www.capstone-engine.org/"
    url      = "https://github.com/aquynh/capstone/archive/4.0.1.tar.gz"

    version('4.0.1', sha256='79bbea8dbe466bd7d051e037db5961fdb34f67c9fac5c3471dd105cfb1e05dc7')
