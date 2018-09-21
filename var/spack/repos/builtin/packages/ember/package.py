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
    """
    Ember Communication Pattern Library
    The Ember suite provides communication patterns in a simplified setting
    (simplified by the removal of application calculations, control flow,
    etc.).
    """

    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "http://sst-simulator.org/SSTPages/SSTElementEmber/"
    git      = "https://github.com/sstsimulator/ember.git"
    url      = "https://github.com/sstsimulator/ember/archive/v1.0.0.tar.gz"

    version('1.0.0', sha256='5b2a6b8055b46ab3ea2c7baabaf4d280d837bb7c21eba0c9f59e092c6fc1c4a6')

    depends_on('mpi')

    # TODO: shmem variant disabled due to lack of shmem spackage
    def edit(self, spec, prefix):
        file = open('Makefile', 'w')

        file.write('CC = mpicc\n')
        file.write('CFLAGS = -O3 -std=c99\n')
        file.write('OSHMEM_CC=cc\n')
        file.write('OSHMEM_C_FLAGS=-O3 -g\n')

        file.write('export CC CFLAGS OSHMEM_CC OSHMEM_C_FLAGS\n')

        file.write('all:\n')
        file.write('\t@$(MAKE) -C mpi/halo3d -f Makefile\n')
        file.write('\t@$(MAKE) -C mpi/halo3d-26 -f Makefile\n')
        file.write('\t@$(MAKE) -C mpi/incast -f Makefile\n')
        file.write('\t@$(MAKE) -C mpi/pingpong -f Makefile\n')
        file.write('\t@$(MAKE) -C mpi/sweep3d -f Makefile\n')
        # file.write('\t@$(MAKE) -C shmem/hotspotinc -f Makefile\n')
        # file.write('\t@$(MAKE) -C shmem/randominc -f Makefile\n')

        file.write('.PHONY: clean\n')
        file.write('clean:\n')
        file.write('\t@$(MAKE) -C mpi/halo3d -f Makefile clean\n')
        file.write('\t@$(MAKE) -C mpi/halo3d-26 -f Makefile clean\n')
        file.write('\t@$(MAKE) -C mpi/incast -f Makefile clean\n')
        file.write('\t@$(MAKE) -C mpi/pingpong -f Makefile clean\n')
        file.write('\t@$(MAKE) -C mpi/sweep3d -f Makefile clean\n')
        # file.write('\t@$(MAKE) -C shmem/hotspotinc -f Makefile clean\n')
        # file.write('\t@$(MAKE) -C shmem/randominc -f Makefile clean\n')

        file.close()

    @property
    def build_targets(self):
        targets = []
        cc = self.spec['mpi'].mpicc
        cflags = '-O3 -std=c99'
        oshmem_cc = 'cc'
        oshmem_c_flags = '-O3 -g'

        targets.append('CC = {0}'.format(cc))
        targets.append('CFLAGS = {0}'.format(cflags))
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
