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


class Minixyce(MakefilePackage):
    """Proxy Application. A portable proxy of some of the key
       capabilities in the electrical modeling Xyce.
    """

    homepage = "https://mantevo.org"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/MiniXyce/miniXyce_1.0.tar.gz"

    tags = ['proxy-app']

    version('1.0', '6fc0e5a561af0b8ff581d9f704194133')

    variant('mpi', default=True, description='Build with MPI Support')

    depends_on('mpi', when='+mpi')

    @property
    def build_targets(self):
        targets = []

        if '+mpi' in self.spec:
            targets.append('CXX={0}'.format(self.spec['mpi'].mpicxx))
            targets.append('LINKER={0}'.format(self.spec['mpi'].mpicxx))
            targets.append('USE_MPI=-DHAVE_MPI -DMPICH_IGNORE_CXX_SEEK')
        else:
            targets.append('CXX=c++')
            targets.append('LINKER=c++')
            targets.append('USE_MPI=')

        # Remove Compiler Specific Optimization Flags
        if '%gcc' not in self.spec:
            targets.append('CPP_OPT_FLAGS=')

        return targets

    def build(self, spec, prefix):
        with working_dir('miniXyce_ref'):
            # Call Script Targets First to Generate Needed Files
            make('generate_info')
            make('common_files')
            make(*self.build_targets)

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('miniXyce_ref/miniXyce.x', prefix.bin)
        install('miniXyce_ref/default_params.txt', prefix.bin)
        install('README', prefix.doc)

        install_tree('miniXyce_ref/tests/', prefix.doc.tests)
