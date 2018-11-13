# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Graph500(MakefilePackage):
    """Graph500 reference implementations."""

    homepage = "https://graph500.org"
    url      = "https://github.com/graph500/graph500/archive/graph500-3.0.0.tar.gz"

    version('3.0.0', 'a2ebb4783b21e2d86387a217776395e3')

    depends_on('mpi@2.0:')

    build_directory = 'src'

    def edit(self, spec, prefix):
        makefile = FileFilter(join_path(self.build_directory, 'Makefile'))
        makefile.filter(r'^MPICC\s*=.*', 'MPICC={0}'.format(spec['mpi'].mpicc))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.bin)
            install('graph500_reference_bfs', prefix.bin)
            install('graph500_reference_bfs_sssp', prefix.bin)
            install('graph500_custom_bfs', prefix.bin)
            install('graph500_custom_bfs_sssp', prefix.bin)
