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
    version('1.0.13', sha256='e85e2e1fe182fe9f504900150d936a06d252a362c591b9d3d8272dd085aa85d9')
    version('1.0.12', sha256='80c926bb6b37288d02e36e07b44e4663841cd1fe541e2cc0b0e44c89ca929759')
    version('1.0.11', sha256='03052194baa220dde7e622a739f09f34393f67ea00a0b163b409d313d7fc7c02')
    version('1.0.10', sha256='6a3cf303e7224b0b32637bd8e2c3c2cf2621f5dbe599cd74ce4b0c215d0fcd2d')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('boost')
    depends_on('mpi', when='+mpi')

    conflicts('%gcc@7.1.0:', when='@:1.0.12')

    def url_for_version(self, version):
        if version > Version('1.0.13'):
            return 'https://github.com/revbayes/revbayes/archive/v{0}.tar.gz'.format(version)
        else:
            return 'https://github.com/revbayes/revbayes.archive/archive/v{0}.tar.gz'.format(version)

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
            if self.spec.version > Version('1.0.13'):
                generate_version = Executable('./generate_version_number.sh')
                generate_version()
                dest = join_path('..', '..', 'src', 'revlanguage', 'utils')
                install('GitVersion.cpp', dest)
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
