##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Lulesh(MakefilePackage):
    """LULESH is a highly simplified application, hard-coded to only
    style typical in scientific C or C++ based applications. Hard
    code to only solve a Sedov blast problem with analytic answer
    """
    tags = ['proxy-app']
    homepage = "https://computation.llnl.gov/projects/co-design/lulesh"
    git      = "https://github.com/LLNL/LULESH.git"

    version('2.0.3', tag='2.0.3')

    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=True, description='Build with OpenMP support')
    variant('visual', default=False,
        description='Build with Visualization support (Silo, hdf5)')

    depends_on('mpi', when='+mpi')
    depends_on('silo', when='+visual')
    depends_on('hdf5', when='+visual')

    @property
    def build_targets(self):
        targets = []
        cxxflag = ' -g -O3 -I. '
        ldflags = ' -g -O3 '
        if '~mpi' in self.spec:
            targets.append('CXX = {0} {1}'.format(spack_cxx, ' -DUSE_MPI=0 '))
        else:
            targets.append(
                'CXX = {0} {1}'.format(self.spec['mpi'].mpicxx,
                                       ' -DUSE_MPI=1'))
            targets.append(
                'MPI_INC = {0}'.format(self.spec['mpi'].prefix.include))
            targets.append('MPI_LIB = {0}'.format(self.spec['mpi'].prefix.lib))
        if '+visual' in self.spec:
            targets.append(
                'SILO_INCDIR = {0}'.format(self.spec['silo'].prefix.include))
            targets.append(
                'SILO_LIBDIR = {0}'.format(self.spec['silo'].prefix.lib))
            cxxflag = ' -g -DVIZ_MESH -I${SILO_INCDIR} '
            ldflags = ' -g -L${SILO_LIBDIR} -Wl,-rpath -Wl, '
            ldflags += '${SILO_LIBDIR} -lsiloh5 -lhdf5 '

        if '+openmp' in self.spec:
            cxxflag += self.compiler.openmp_flag
            ldflags += self.compiler.openmp_flag

        targets.append('CXXFLAGS = {0}'.format(cxxflag))
        targets.append('LDFLAGS = {0}'.format(ldflags))
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('lulesh{0}'.format(self.version.up_to(2)), prefix.bin)
        mkdirp(prefix.doc)
        install('README', prefix.doc)
        install('TODO', prefix.doc)
