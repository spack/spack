# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BaseWithDirectives(Package):

    depends_on('cmake', type='build')
    depends_on('mpi')
    variant('openblas', description='Activates openblas', default=True)
    provides('service1')


class SimpleInheritance(BaseWithDirectives):
    """Simple package which acts as a build dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/simple-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('openblas', when='+openblas')
    provides('lapack', when='+openblas')

    def install(self, spec, prefix):
        pass
