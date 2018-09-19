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


class Revbayes(CMakePackage):
    """Bayesian phylogenetic inference using probabilistic graphical models
       and an interpreted language."""

    homepage = "https://revbayes.github.io"
    url      = "https://github.com/revbayes/revbayes/archive/v1.0.4-release.tar.gz"

    version('1.0.4', '5d6de96bcb3b2686b270856de3555a58')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('boost')
    depends_on('mpi', when='+mpi')

    conflicts('%gcc@7.1.0:')

    root_cmakelists_dir = 'projects/cmake/build'

    @run_before('cmake')
    def regenerate(self):
        with working_dir(join_path('projects', 'cmake')):
            mkdirp('build')
            edit = FileFilter('regenerate.sh')
            edit.filter('boost="true"', 'boost="false"')
            if '+mpi' in self.spec:
                edit.filter('mpi="false"', 'mpi="true"')
            regenerate = Executable('./regenerate.sh')
            regenerate()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if '+mpi' in spec:
            install('rb-mpi', prefix.bin)
        else:
            install('rb', prefix.bin)
