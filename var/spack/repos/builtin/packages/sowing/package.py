# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Sowing(AutotoolsPackage):
    """Sowing generates Fortran interfaces and documentation for PETSc
       and MPICH.
    """

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url = "http://ftp.mcs.anl.gov/pub/petsc/externalpackages/sowing-1.1.23-p1.tar.gz"

    version('1.1.25-p1', 'fc5e5664b80e606ad71ba9b85f4c86b9')
    version('1.1.23-p1', '65aaf3ae2a4c0f30d532fec291702e16')

    def build(self, spec, prefix):
        make('ALL', parallel=False)
