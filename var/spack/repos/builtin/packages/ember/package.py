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


class Ember(MakefilePackage):
    """Ember Communication Pattern Library

       The Ember suite provides communication patterns in a simplified setting
       (simplified by the removal of application calculations, control flow
       etc.).
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "http://sst-simulator.org/SSTPages/SSTElementEmber/"
    git      = "https://github.com/sstsimulator/ember.git"
    url      = "https://github.com/sstsimulator/ember/archive/v1.0.0.tar.gz"

    version('1.0.0', sha256='5b2a6b8055b46ab3ea2c7baabaf4d280d837bb7c21eba0c9f59e092c6fc1c4a6')

    variant('halo3d', default=True, description='Halo3d motif')
    variant('halo3d-26', default=False, description='Halo3d-26 motif')
    variant('incast', default=False, description='Incast motif')
    variant('pingpong', default=False, description='Pingpong motif')
    variant('sweep3d', default=False, description='Sweep3d motif')

    variant('hotspotinc', default=False, description='Hotspotinc motif')
    variant('randominc', default=False, description='Randominc motif')

    depends_on('mpi', when='+halo3d')
    depends_on('mpi', when='+halo3d-26')
    depends_on('mpi', when='+incast')
    depends_on('mpi', when='+pingpong')
    depends_on('mpi', when='+sweep3d')

    @property
    def build_targets(self):
        targets = []
        cc = self.spec['mpi'].mpicc
        cflags = '-O3 -std=c99'
        oshmem_cc = 'cc'
        oshmem_c_flags = '-O3 -g'

        if '+halo3d' in self.spec:
            targets.append('--directory=mpi/halo3d')
            targets.append('CC = {0}'.format(cc))
            targets.append('CFLAGS = {0}'.format(cflags))
        elif '+halo3d-26' in self.spec:
            targets.append('--directory=mpi/halo3d-26')
            targets.append('CC = {0}'.format(cc))
            targets.append('CFLAGS = {0}'.format(cflags))
        elif '+incast' in self.spec:
            targets.append('--directory=mpi/incast')
            targets.append('CC = {0}'.format(cc))
            targets.append('CFLAGS = {0}'.format(cflags))
        elif '+pingpong' in self.spec:
            targets.append('--directory=mpi/pingpong')
            targets.append('CC = {0}'.format(cc))
            targets.append('CFLAGS = {0}'.format(cflags))
        elif '+sweep3d' in self.spec:
            targets.append('--directory=mpi/sweep3d')
            targets.append('CC = {0}'.format(cc))
            targets.append('CFLAGS = {0}'.format(cflags))
        elif '+hotspotinc' in self.spec:
            targets.append('--directory=shmem/hotspotinc')
            targets.append('OSHMEM_CC = {0}'.format(oshmem_cc))
            targets.append('OSHMEM_C_FLAGS = {0}'.format(oshmem_c_flags))
        elif '+randominc' in self.spec:
            targets.append('--directory=shmem/randominc')
            targets.append('OSHMEM_CC = {0}'.format(oshmem_cc))
            targets.append('OSHMEM_C_FLAGS = {0}'.format(oshmem_c_flags))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
        install('LICENSE', prefix.doc)
        install('README.MPI.halo3d', prefix.doc)
        install('README.MPI.halo3d-26', prefix.doc)
        install('README.MPI.incast', prefix.doc)
        install('README.MPI.sweep3d', prefix.doc)
        install('README.SHMEM.hotspotinc', prefix.doc)
        install('README.SHMEM.randominc', prefix.doc)
