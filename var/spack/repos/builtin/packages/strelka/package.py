# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Strelka(CMakePackage):
    """Somatic and germline small variant caller for mapped sequencing
       data."""

    homepage = "https://github.com/Illumina/strelka"
    url      = "https://github.com/Illumina/strelka/releases/download/v2.8.2/strelka-2.8.2.release_src.tar.bz2"

    version('2.8.2', sha256='27415f7c14f92e0a6b80416283a0707daed121b8a3854196872981d132f1496b')

    depends_on('python@2.4:2.7')
    depends_on('zlib')
    depends_on('bzip2')
    depends_on('cmake@2.8.5:')
    depends_on('boost@1.56.0:')
