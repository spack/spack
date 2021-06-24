# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Simgrid(CMakePackage):
    """To study the behavior of large-scale distributed systems such as Grids,
    Clouds, HPC or P2P systems."""

    homepage = "http://simgrid.org/"
    url      = "https://github.com/simgrid/simgrid/releases/download/v3.27/simgrid-3.27.tar.gz"
    git      = 'https://framagit.org/simgrid/simgrid.git'

    version('3.27', sha256 = '51aeb9de0434066e5fec40e785f5ea9fa934afe7f6bfb4aa627246e765f1d6d7',
            url = 'https://github.com/simgrid/simgrid/releases/download/v3.27/simgrid-3.27.tar.gz')
    version('3.26', sha256 = 'ac50da1eacc5a53b094a988a8ecde09962c29320f346b45e74dd32ab9d9f3e96',
            url = "https://github.com/simgrid/simgrid/releases/download/v3.26/simgrid-3.26.tar.gz")
    version('3.25', sha256='0b5dcdde64f1246f3daa7673eb1b5bd87663c0a37a2c5dcd43f976885c6d0b46',
            url = 'https://github.com/simgrid/simgrid/releases/download/v3.25/SimGrid-3.25.tar.gz')
    version('3.24', sha256='c976ed1cbcc7ff136f6d1a8eda7d9ccf090e0e16d5239e6e631047ae9e592921',
            url = 'https://github.com/simgrid/simgrid/releases/download/v3.24/SimGrid-3.24.tar.gz')
    version('3.23', sha256='c3c86673abf0a2685337f1f520a7782d9611cd18d0374f35e1d98652fdbbaf86',
            url = 'https://github.com/simgrid/simgrid/releases/download/v3.23/SimGrid-3.23.tar.gz')
    version('3.22', sha256='4fdff0a8e4c81f8edf6f7eedfa32e19748abe688d156ea9240178c558c8bad33',
            url = 'https://github.com/simgrid/simgrid/releases/download/v3_22/SimGrid-3.22.tar.gz')
    version('3.21', sha256='d2a6e9021016dd39a2b6f8d5d18c8223f6885746c5269550d19ba29c47c0c6a0',
            url = 'https://github.com/simgrid/simgrid/releases/download/v3_21/SimGrid-3.21.tar.gz')
    version('3.20', sha256='4d4757eb45d87cf18d990d589c31d223b0ea8cf6fcd8c94fca4d38162193cef6',
            url = 'https://github.com/simgrid/simgrid/releases/download/v3.20/SimGrid-3.20.tar.gz')

    version('develop', branch='master')

    variant('doc', default=False, description='Build documentation')
    variant('smpi', default=True, description='SMPI provides MPI')
    variant('examples', default=False, description='Install examples')
    variant('mc', default=False, description='Model checker')

    # does not build correctly with some old compilers -> rely on packages
    depends_on('boost')
    depends_on('boost@:1.69.0', when = '@:3.21')

    conflicts('%gcc@10:', when='@:3.23',
          msg='<simgrid <= v3.23 cannot be built with gcc >= 10, please use an older release (e.g., %gcc@:9.99).')


    def setup_dependent_package(self, module, dep_spec):

        if self.spec.satisfies('+smpi'):
            self.spec.smpicc  = join_path(self.prefix.bin, 'smpicc')
            self.spec.smpicxx = join_path(self.prefix.bin,
                                          'smpicxx -std=c++11')
            self.spec.smpifc  = join_path(self.prefix.bin, 'smpif90')
            self.spec.smpif77 = join_path(self.prefix.bin, 'smpiff')

    def cmake_args(self):

        spec = self.spec
        args = []

        if not spec.satisfies('+doc'):
            args.append("-Denable_documentation=OFF")
        if spec.satisfies('+mc'):
            args.append("-Denable_model-checking=ON")

        return args

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            make("install")
            if spec.satisfies('+examples'):
                install_tree(join_path(self.build_directory, 'examples'),
                             prefix.examples)
