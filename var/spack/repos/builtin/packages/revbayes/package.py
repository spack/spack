# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Revbayes(CMakePackage):
    """Bayesian phylogenetic inference using probabilistic graphical models
       and an interpreted language."""

    homepage = "https://revbayes.github.io"
    url      = "https://github.com/revbayes/revbayes/archive/v1.0.11.tar.gz"
    git      = "https://github.com/revbayes/revbayes.git"

    version('develop', branch='development')
    version('1.0.13', sha256='472b4ccc44d813c1ff1b8d27e8ccf3d96388de79aa1688b3714f683ba65038fa')
    version('1.0.12', sha256='d79f3a9bc72305cab35009d11e1f027fcaacde7329a4c49b5b8285588a8d3588')
    version('1.0.11', sha256='7e81b1952e3a63cb84617fa632f4ccdf246b4d79e7d537a423540de047dadf50')
    version('1.0.10', sha256='95e9affe8ca8d62880cf46778b6ec9dd8726e62a185670ebcbadf2eb2bb79f93')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('boost')
    depends_on('mpi', when='+mpi')

    conflicts('%gcc@7.1.0:', when='@:1.0.12')

    @property
    def root_cmakelists_dir(self):
        if self.spec.version > Version('1.0.13') and '+mpi' in self.spec:
            return 'projects/cmake/build-mpi'
        else:
            return 'projects/cmake/build'

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
            install_path = join_path(self.build_directory, '..', 'rb-mpi')
            install(install_path, prefix.bin)
        else:
            install_path = join_path(self.build_directory, '..', 'rb')
            install(install_path, prefix.bin)

    @when('@1.0.12:1.0.13')
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_path = join_path(self.build_directory, '..', 'rb')
        install(install_path, prefix.bin)
