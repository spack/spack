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


class Hpccg(MakefilePackage):
    """Proxy Application. Intended to be the 'best approximation
       to an unstructured implicit finite element or finite volume
       application in 800 lines or fewer.'
    """

    homepage = "https://mantevo.org/about/applications/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/HPCCG/HPCCG-1.0.tar.gz"

    tags = ['proxy-app']

    version('1.0', '2e99da1a89de5ef0844da5e6ffbf39dc')

    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=True, description='Build with OpenMP support')

    # Optional dependencies
    depends_on('mpi', when='+mpi')

    @property
    def build_targets(self):
        targets = []

        if '+mpi' in self.spec:
            targets.append('CXX={0}'.format(self.spec['mpi'].mpicxx))
            targets.append('LINKER={0}'.format(self.spec['mpi'].mpicxx))
            targets.append('USE_MPI=-DUSING_MPI')
        else:
            targets.append('CXX=c++')
            targets.append('LINKER=c++')

        if '+openmp' in self.spec:
            targets.append('USE_OMP=-DUSING_OMP')
            targets.append('OMP_FLAGS={0}'.format(self.compiler.openmp_flag))

        # Remove Compiler Specific Optimization Flags
        if '%gcc' not in self.spec:
            targets.append('CPP_OPT_FLAGS=')

        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('test_HPCCG', prefix.bin)
        install('README', prefix.doc)
        install('weakScalingRunScript', prefix.bin)
        install('strongScalingRunScript', prefix.bin)
