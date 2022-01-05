##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from tempfile import TemporaryFile

import os
from os.path import dirname
import stat

from llnl.util.filesystem import find
from spack import *


class HpeMpi(Package):
    """HPE-SGI MPI package"""

    homepage = "http://www.no-name.com"
    url      = "http://www.no-name.com/hpempi-1.0.tar.gz"

    version('2.21',
            sha256='2f27ad2e92ef0004b9a4dfb3b76837d1b657c43ff89f4deef99be58a322a80b7',
            url='file:///gpfs/bbp.cscs.ch/apps/hpc/download/hpe-mpi/hpe-mpi-2.21.tar.xz')
    version('2.22',
            sha256='258eb3714b09254911be7b30baec8ccbebbd84f4a9301d817c862e5a4051edea',
            url='file:///gpfs/bbp.cscs.ch/apps/hpc/download/hpe-mpi/hpe-mpi-2.22.tar.xz')
    version('2.21.hmpt',
            sha256='27aa203ff8820e2db3672a59dd0c681b4affffa466255712ed1b32a0c6c8efb1',
            url='file:///gpfs/bbp.cscs.ch/apps/hpc/download/hpe-mpi/hpe-mpi-2.21.hmpt.tar.xz')
    version('2.22.hmpt',
            sha256='e067e4ba382d306d540e1ad5bcd63035a4aa93e7d7c15d617e82de4160e5ad8a',
            url='file:///gpfs/bbp.cscs.ch/apps/hpc/download/hpe-mpi/hpe-mpi-2.22.hmpt.tar.xz')
    version('2.25.hmpt',
            sha256='126a46bb2cbd4b63bd7b3aed74cee5e8d08e166e9748071fd0b308be29335e1a',
            url='file:///gpfs/bbp.cscs.ch/apps/hpc/download/hpe-mpi/hpe-mpi-2.25.hmpt.tar.xz')

    provides('mpi')

    @run_before('install')
    def unpack(self):
        rpm2cpio = spack.util.executable.which('rpm2cpio')
        cpio = spack.util.executable.which('cpio')
        chmod = spack.util.executable.which('chmod')

        print(self.stage)
        for rpm_filename in find(self.stage.source_path, '*.rpm'):
            with TemporaryFile() as tmpf:
                rpm2cpio(rpm_filename, output=tmpf)
                tmpf.seek(0)
                cpio('-dium', input=tmpf)
        chmod('-R', 'u+w', self.stage.source_path)

    def install(self, spec, prefix):
        for mpic in find(self.stage.source_path, 'mpic*'):
            if os.path.isfile(mpic):
                mode = os.stat(mpic).st_mode
                os.chmod(mpic, mode | stat.S_IWRITE)
                filter_file(
                    r'-I(.*mpiroot)',
                    r'-isystem \1',
                    mpic
                )

        root_dir = dirname(dirname(find(self.stage.source_path, 'mpicc')[0]))
        install_tree(root_dir, prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        bindir = self.prefix.bin
        env.set('MPICC',  join_path(bindir, 'mpicc'))
        env.set('MPICXX', join_path(bindir, 'mpicxx'))
        env.set('MPIF77', join_path(bindir, 'mpif77'))
        env.set('MPIF90', join_path(bindir, 'mpif90'))

        env.set('MPICC_CC', spack_cc)
        env.set('MPICXX_CXX', spack_cxx)
        env.set('MPIF90_F90', spack_fc)

        env.set('MPI_ROOT', self.prefix)

        env.append_path('LD_LIBRARY_PATH', self.prefix.lib)

    def setup_dependent_package(self, module, dep_spec):
        bindir = self.prefix.bin
        self.spec.mpicc = join_path(bindir, 'mpicc')
        self.spec.mpicxx = join_path(bindir, 'mpicxx')
        self.spec.mpifc = join_path(bindir, 'mpif77')
        self.spec.mpif77 = join_path(bindir, 'mpif90')
