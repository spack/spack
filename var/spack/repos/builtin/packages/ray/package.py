# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ray(CMakePackage):
    """Parallel genome assemblies for parallel DNA sequencing"""

    homepage = "http://denovoassembler.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/denovoassembler/Ray-2.3.1.tar.bz2"

    version('2.3.1', '82f693c4db60af4328263c9279701009')

    depends_on('mpi')

    @run_after('build')
    def make(self):
        mkdirp(prefix.bin)
        make('PREFIX=%s' % prefix.bin)

    def install(self, spec, prefix):
        make('install')
