# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install optpp
#
# You can edit this file again by typing:
#
#     spack edit optpp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Optpp(AutotoolsPackage):
    """OPT++ is a C++ library of nonlinear optimization algorithms.
    """

    homepage = "https://software.sandia.gov/opt++"
    url      = "https://github.com/openturns/optpp/archive/v2.4.tar.gz"

    version('2.4', sha256='0f0cd0287eeb80123a7b1700ecf434bb662c35b5cc177312b94f2099695529e8')

    variant('mpi', default=False, description='Enable mpi support')
    variant('blas', default=False, description='Enable BLAS library')

    depends_on('mpi', when='+mpi')
    depends_on('blas', when='+blas')

    def configure_args(self):
        spec = self.spec

        args = [
            '--enable-shared'
        ]

        if '+mpi' in spec:
            args.append('--enable-mpi')

        if '+blas' in spec:
            args.append('--with-blas=%s' % spec['blas'].libs)

        return args
