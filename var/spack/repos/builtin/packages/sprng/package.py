# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install sprng
#
# You can edit this file again by typing:
#
#     spack edit sprng
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Sprng(AutotoolsPackage):

    # A list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['gmfricke', 'patrickb314']

    homepage = "https://www.sprng.org"
    url      = "http://www.sprng.org/Version5.0/sprng5.tar.bz2"

    version('5', sha256='9172a495472cc24893e7489ce9b5654300dc60cba4430e436ce50d28eb749a66')

    variant('mpi', default=True, description='Enable MPI support')
    variant('fortran', default=False, description='Enable Fortran support')

    depends_on('mpi', when='+mpi')
    depends_on('fortran', when='+fortran')

    def configure_args(self):
        args = []
        spec = self.spec

        if '+fortran' not in spec:
            args.append('--with-fortran=no')

        if '+mpi' in spec:
            args.append('--with-mpi')
            if spec.satisfies('^openmpi'):
                args.append('LIBS=-lmpi_cxx')

        return args
