# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpileaks(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version(1.0, '0123456789abcdef0123456789abcdef')
    version(2.1, '0123456789abcdef0123456789abcdef')
    version(2.2, '0123456789abcdef0123456789abcdef')
    version(2.3, '0123456789abcdef0123456789abcdef')

    variant('debug', default=False, description='Debug variant')
    variant('opt',   default=False, description='Optimized variant')
    variant('shared', default=True, description='Build shared library')
    variant('static', default=True, description='Build static library')

    depends_on("mpi")
    depends_on("callpath")

    # Will be used to try raising an exception
    libs = None

    def install(self, spec, prefix):
        touch(prefix.mpileaks)

    def setup_environment(self, senv, renv):
        renv.set('FOOBAR', self.name)
