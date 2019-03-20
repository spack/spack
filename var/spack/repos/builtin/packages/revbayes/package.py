# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Revbayes(CMakePackage):
    """Bayesian phylogenetic inference using probabilistic graphical models
       and an interpreted language."""

    homepage = "https://revbayes.github.io"
    url      = "https://github.com/revbayes/revbayes/archive/v1.0.10.tar.gz"

    version('1.0.10', sha256='95e9affe8ca8d62880cf46778b6ec9dd8726e62a185670ebcbadf2eb2bb79f93')
    version('1.0.4', '5d6de96bcb3b2686b270856de3555a58',
            url='https://github.com/revbayes/revbayes/archive/v1.0.4-release.tar.gz')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('boost')
    depends_on('mpi', when='+mpi')

    conflicts('%gcc@7.1.0:')

    root_cmakelists_dir = 'projects/cmake/build'

    @run_before('cmake')
    def regenerate(self):
        with working_dir(join_path('projects', 'cmake')):
            mkdirp('build')
            edit = FileFilter('regenerate.sh')
            edit.filter('boost="true"', 'boost="false"')
            if '+mpi' in self.spec:
                edit.filter('mpi="false"', 'mpi="true"')
            regenerate = Executable('./regenerate.sh')
            regenerate()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if '+mpi' in spec:
            install('rb-mpi', prefix.bin)
        else:
            install('rb', prefix.bin)
