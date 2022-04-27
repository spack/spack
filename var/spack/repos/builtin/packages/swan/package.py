# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Swan(MakefilePackage):
    """SWAN is a third-generation wave model, developed at Delft
    University of Technology, that computes random, short-crested
     wind-generated waves in coastal regions and inland waters.
    For more information about SWAN, see a short overview of model
    features. This list reflects on the scientific relevance of
    the development of SWAN."""

    homepage = "http://swanmodel.sourceforge.net/"
    url = "https://cfhcable.dl.sourceforge.net/project/swanmodel/swan/41.31/swan4131.tar.gz"

    maintainers = ['lhxone']

    version('4131', sha256='cd3ba1f0d79123f1b7d42a43169f07575b59b01e604c5e66fbc09769e227432e')

    depends_on('mpi')
    depends_on('netcdf-fortran')
    depends_on('libfabric')

    def edit(self, spec, prefix):
        env['FC'] = 'gfortran'
        m = FileFilter('platform.pl')
        m.filter('F90_MPI = .*', 'F90_MPI = mpifort\\n";')
        m.filter('NETCDFROOT =', 'NETCDFROOT = {0}' + spec['netcdf-fortran'].prefix)

    def build(self, spec, prefix):
        make('config')
        make('mpi')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('*.exe', prefix.bin)
