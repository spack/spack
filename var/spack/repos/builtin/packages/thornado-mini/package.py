##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC.
# Produced at the Los Alamos National Laboratory.
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
import os


class ThornadoMini(MakefilePackage):
    """Code to solve the equation of radiative transfer in the
    multi-group two-moment approximation"""

    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://sites.google.com/lbl.gov/exastar/home"
    url      = "https://github.com/ECP-Astro/thornado_mini/archive/v1.0.tar.gz"
    git      = "https://github.com/ECP-Astro/thornado_mini.git"

    version('1.0', sha256='8a9f97acc823d374cce567831270cfcc50fa968949e49159c7e3442b93a2827d')

    depends_on('mpi')
    depends_on('hdf5+fortran')
    depends_on('lapack')

    parallel = False

    def edit(self, spec, prefix):
        os.environ['THORNADO_MACHINE'] = 'mymachine'
        os.environ['THORNADO_DIR'] = os.getcwd()

        file = open('Makefile', 'w')

        file.write('FORTRAN_mymachine = %s %s\n' % (self.spec['mpi'].mpifc,
                                                    self.compiler.openmp_flag))
        file.write('FLINKER_mymachine = %s %s\n' % (self.spec['mpi'].mpifc,
                                                    self.compiler.openmp_flag))
        file.write('DEBUG_mymachine = -g -ffpe-trap=invalid,zero \
        -fcheck=bounds\n')
        file.write('OPTIMIZE_mymachine = -O2\n')
        file.write('INCLUDE_HDF5_mymachine = \n')
        file.write('INCLUDE_LAPACK_mymachine = \n')
        file.write('LIBRARIES_HDF5_mymachine = \n')
        file.write('LIBRARIES_LAPACK_mymachine = \n')
        file.write('export FORTRAN_mymachine FLINKER_mymachine \
        DEBUG_mymachine OPTIMIZE_mymachine\n')

        file.write('all:\n')
        file.write('\t@$(MAKE) -C $(THORNADO_DIR)/DeleptonizationProblem/Executables \
        -f Makefile\n')

        file.close()

    @property
    def build_targets(self):
        targets = []

        targets.append('INCLUDE_HDF5_mymachine = -I{0}'
                       .format(self.spec['hdf5'].prefix.include))
        targets.append('INCLUDE_LAPACK_mymachine = -I{0}'
                       .format(self.spec['lapack'].prefix.include))
        targets.append('LIBRARIES_HDF5_mymachine = {0} -lhdf5_fortran'
                       .format(self.spec['hdf5'].libs.ld_flags))
        targets.append('LIBRARIES_LAPACK_mymachine = {0}'
                       .format(self.spec['lapack'].libs.ld_flags))

        return targets

    def install(self, spec, prefix):
        install_tree('Documents', prefix.docs)
        install('README.md', prefix.docs)

        mkdirp(prefix.bin)
        install('DeleptonizationProblem/Executables/'
                'DeleptonizationProblem1D_%s' %
                os.environ['THORNADO_MACHINE'], prefix.bin)
