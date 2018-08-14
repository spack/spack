##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC
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


class Examinimd(MakefilePackage):
    """ExaMiniMD is a proxy application and research vehicle for particle codes,
    in particular Molecular Dynamics (MD). Compared to previous MD proxy apps
    (MiniMD, COMD), its design is significantly more modular in order to allow
    independent investigation of different aspects. To achieve that the main
    components such as force calculation, communication, neighbor list
    construction and binning are derived classes whose main functionality is
    accessed via virtual functions. This allows a developer to write a new
    derived class and drop it into the code without touching much of the
    rest of the application."""

    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://github.com/ECP-copa/ExaMiniMD"
    url      = "https://github.com/ECP-copa/ExaMiniMD/archive/1.0.zip"
    git      = "https://github.com/ECP-copa/ExaMiniMD.git"

    version('develop', branch='master')
    version('1.0', '5db7679a4b9296c0cc3b2ff3a7e8f38f')

    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=False, description='Build with OpenMP support')
    variant('pthreads', default=False, description='Build with POSIX Threads support')
    # TODO: Set up cuda variant when test machine available

    conflicts('+openmp', when='+pthreads')

    depends_on('kokkos')
    depends_on('mpi', when='+mpi')

    @property
    def build_targets(self):
        targets = []
        # Append Kokkos
        targets.append('KOKKOS_PATH={0}'.format(self.spec['kokkos'].prefix))
        # Set kokkos device
        if 'openmp' in self.spec:
            targets.append('KOKKOS_DEVICES=OpenMP')
        elif 'pthreads' in self.spec:
            targets.append('KOKKOS_DEVICES=Pthread')
        else:
            targets.append('KOKKOS_DEVICES=Serial')
        # Set MPI as needed
        if '+mpi' in self.spec:
            targets.append('MPI=1')
            targets.append('CXX = {0}'.format(self.spec['mpi'].mpicxx))
        else:
            targets.append('MPI=0')
            targets.append('CXX = {0}'.format('spack_cxx'))
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('src/ExaMiniMD', prefix.bin)
        install_tree('input', prefix.input)
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
        install('LICENSE', prefix.doc)
