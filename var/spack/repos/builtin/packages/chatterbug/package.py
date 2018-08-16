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


class Chatterbug(MakefilePackage):
    """A suite of communication-intensive proxy applications that mimic
       commonly found communication patterns in HPC codes. These codes can be
       used as synthetic codes for benchmarking, or for trace generation using
       OTF2.
    """
    tags = ['proxy-app']

    homepage = "https://chatterbug.readthedocs.io"
    git      = "https://github.com/LLNL/chatterbug.git"

    version('develop', branch='master')
    version('1.0', tag='v1.0')

    variant('otf2', default=False, description='Build with OTF2 tracing')

    depends_on('mpi')
    depends_on('scorep~gui', when='+otf2')

    @property
    def build_targets(self):
        targets = []

        cxxflag = ' -O3 '

        if '+otf2' in self.spec:
            cxxflag += '-I{0}'.format(spec['scorep'].prefix.include)
            cxxflag += '-I{0}/scorep'.format(spec['scorep'].prefix.include)
            cxxflag += '-DWRITE_OTF2_TRACE=1 -DSCOREP_USER_ENABLE'
            targets.append(
                'CXX = {0} {1}'.format('scorep --user --nocompiler ' \
                                       '--noopenmp --nopomp --nocuda ' \
                                       '--noopenacc --noopencl --nomemory',
                                       self.spec['mpi'].mpicxx))
        else:
            targets.append('CXX = {0}'.format(self.spec['mpi'].mpicxx))

        targets.append('CXXFLAGS = {0}'.format(cxxflag))
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        if '+otf2' in self.spec:
            install('pairs/pairs.otf2', prefix.bin)
            install('ping-ping/ping-ping.otf2', prefix.bin)
            install('spread/spread.otf2', prefix.bin)
            install('stencil3d/stencil3d.otf2', prefix.bin)
            install('stencil4d/stencil4d.otf2', prefix.bin)
            install('subcom2d-coll/subcom2d-coll.otf2', prefix.bin)
            install('subcom3d-a2a/subcom3d-a2a.otf2', prefix.bin)
            install('unstr-mesh/unstr-mesh.otf2', prefix.bin)
        else:
            install('pairs/pairs.x', prefix.bin)
            install('ping-ping/ping-ping.x', prefix.bin)
            install('spread/spread.x', prefix.bin)
            install('stencil3d/stencil3d.x', prefix.bin)
            install('stencil4d/stencil4d.x', prefix.bin)
            install('subcom2d-coll/subcom2d-coll.x', prefix.bin)
            install('subcom3d-a2a/subcom3d-a2a.x', prefix.bin)
            install('unstr-mesh/unstr-mesh.x', prefix.bin)
