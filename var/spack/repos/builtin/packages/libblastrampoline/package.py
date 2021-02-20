# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libblastrampoline(Package):
    """Using PLT trampolines to provide a BLAS and LAPACK demuxing library."""

    homepage = "https://github.com/staticfloat/libblastrampoline"
    git      = "https://github.com/staticfloat/libblastrampoline.git"

    version('2.2.0', commit='45f4a20ffdba5d368db66d71885312f5f73c2dc7')

    def build(self, spec, prefix):
        make('-C', 'src')

    def install(self, spec, prefix):
        make('-C', 'src', 'prefix={0}'.format(prefix), 'install')
