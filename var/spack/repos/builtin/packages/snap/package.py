##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Snap(MakefilePackage):
    """SNAP serves as a proxy application to model
    the performance of a modern discrete ordinates
    neutral particle transport application.
    SNAP may be considered an update to Sweep3D,
    intended for hybrid computing architectures.
    It is modeled off the Los Alamos National Laboratory code PARTISN."""

    homepage = "https://github.com/lanl/SNAP"
    git      = "https://github.com/lanl/SNAP.git"

    tags = ['proxy-app']

    version('master')

    variant('openmp', default=False, description='Build with OpenMP support')
    variant('opt', default=True, description='Build with debugging')
    variant('mpi', default=True, description='Build with MPI support')

    depends_on('mpi', when='+mpi')

    build_directory = 'src'

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            if '~opt' in spec:
                makefile.filter('OPT = yes', 'OPT = no')
            if '~mpi' in spec:
                makefile.filter('MPI = yes', 'MPI = no')
            if '~openmp' in spec:
                makefile.filter('OPENMP = yes', 'OPENMP = no')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('src/gsnap', prefix.bin)
        install_tree('qasnap', prefix.qasnap)
        install('README.md', prefix)
