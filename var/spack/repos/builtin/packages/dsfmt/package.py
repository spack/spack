# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dsfmt(MakefilePackage):
    """Double precision SIMD-oriented Fast Mersenne Twister"""

    homepage = "http://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/SFMT/"
    url      = "http://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/SFMT/dSFMT-src-2.2.3.tar.gz"

    maintainers = ['haampie']

    # This package does not have a target to build a library nor a make install target,
    # so we add it for them.
    patch('targets.patch')

    version('2.2.3', sha256='82344874522f363bf93c960044b0a6b87b651c9565b6312cf8719bb8e4c26a0e')

    @property
    def libs(self):
        return find_libraries('libdSFMT', root=self.prefix, recursive=True)

    def make(self, spec, prefix):
        make('library')

    def install(self, spec, prefix):
        make('PREFIX={0}'.format(prefix), 'install')
