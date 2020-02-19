##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from tempfile import TemporaryFile

import os
import stat

from llnl.util.filesystem import find
from spack import *


class HpeMpi(Package):
    """HPE-SGI MPI package"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/hpempi-1.0.tar.gz"

    version('2.21', '2dd6c53a82993c4df929fdf898ac3d19',
        url='file:///gpfs/bbp.cscs.ch/apps/hpc/download/hpe-mpi/hpe-mpi-2.21.tar.xz')

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
            mode = os.stat(mpic).st_mode
            os.chmod(mpic, mode | stat.S_IWRITE)
            filter_file(r'-I(.*mpiroot)', r'-isystem\1', mpic)

        install_tree(
            join_path(self.stage.source_path,
                      'opt/hpe/hpc/mpt/mpt-' + str(self.spec.version)),
            prefix
        )

    def setup_dependent_build_environment(self, env, dependent_spec):
        bindir = self.prefix.bin
        env.set('MPICC',  join_path(bindir, 'mpicc'))
        env.set('MPICXX', join_path(bindir, 'mpicxx'))
        env.set('MPIF77', join_path(bindir, 'mpif77'))
        env.set('MPIF90', join_path(bindir, 'mpif90'))

        env.set('MPICC_CC', spack_cc)
        env.set('MPICXX_CXX', spack_cxx)
        env.set('MPIF90_F90', spack_fc)

    def setup_dependent_package(self, module, dep_spec):
        bindir = self.prefix.bin
        self.spec.mpicc = join_path(bindir, 'mpicc')
        self.spec.mpicxx = join_path(bindir, 'mpicxx')
        self.spec.mpifc = join_path(bindir, 'mpif77')
        self.spec.mpif77 = join_path(bindir, 'mpif90')
