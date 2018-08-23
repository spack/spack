##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
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


class Coevp(MakefilePackage):
    """CoEVP is a scale-bridging proxy application for embedded viscoplasticity
    applications. It is created and maintained by The Exascale Co-Design Center
    for Materials in Extreme Environments (ExMatEx). The code is intended to
    serve as a vehicle for co-design by allowing others to extend and/or
    reimplement it as needed to test performance of new architectures,
    programming models, etc.
    Due to the size and complexity of the studied models, as well as
    restrictions on distribution, the currently available LULESH proxy
    application provides the coarse-scale model implementation and the ASPA
    proxy application provides the adaptive sampling support."""

    homepage = 'https://github.com/exmatex/CoEVP'
    git      = 'https://github.com/exmatex/CoEVP.git'

    version('develop', branch='master')

    variant('mpi', default=True, description='Build with MPI Support')
    variant('silo', default=False, description='Build with silo Support')
    variant('flann', default=False, description='Build with flann Support')

    depends_on('mpi', when='+mpi')
    depends_on('silo', when='+silo')
    depends_on('flann@1.8.1', when='+flann')
    depends_on('lapack')

    tags = ['proxy-app']

    @property
    def build_targets(self):
        targets = []
        if '+mpi' in self.spec:
            targets.append('COEVP_MPI=yes')
        else:
            targets.append('COEVP_MPI=no')
        if '+flann' in self.spec:
            targets.append('FLANN=yes')
            targets.append('FLANN_TARGET=')
            targets.append('FLANN_LOC={0}'.format(
                join_path(self.spec['flann'].prefix.include, 'flann')))
        else:
            targets.append('FLANN=no')
        targets.append('REDIS=no')
        if '+silo' in self.spec:
            targets.append('SILO=yes')
            targets.append('SILO_TARGET=')
            targets.append('SILO_LOC={0}'.format(self.spec['silo'].prefix))
        else:
            targets.append('SILO=no')
        targets.append('TWEMPROXY=no')
        targets.append('LAPACK=%s' % self.spec['lapack'].libs.ld_flags)

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        install('LULESH/lulesh', prefix.bin)
        install('COPYRIGHT', prefix.doc)
        install('README.md', prefix.doc)
        install('CoEVP.pdf', prefix.doc)
