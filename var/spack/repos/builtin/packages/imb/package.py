##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
from shutil import copyfile
import os


class Imb(MakefilePackage):
    """Intel MPI Benchmark"""

    homepage = "https://github.com/intel/mpi-benchmarks.git"
    url      = "https://github.com/intel/mpi-benchmarks.git"

    version('master',  git=url)

    depends_on('mpi')

    def edit(self, spec, prefix):
        os.chdir("src")
        makefile = FileFilter('make_ict')
        makefile.filter('CC          = .*', 'CC = %s'
                        % self.spec['mpi'].mpicc)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        imb = join_path(prefix.bin, "IMB-MPI1")
        copyfile("IMB-MPI1", imb)
        chmod = which('chmod')
        chmod('+x', imb)
