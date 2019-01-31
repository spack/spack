# Copyright 2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Simgrid(CMakePackage):
    """To study the behavior of large-scale distributed systems such as Grids,
    Clouds, HPC or P2P systems."""

    homepage = "http://simgrid.org/"
    url      = "https://gforge.inria.fr/frs/download.php/file/37758/SimGrid-3.21.tar.gz"
    git      = 'https://scm.gforge.inria.fr/anonscm/git/simgrid/simgrid.git'

    version('3.21', '6a5664f20433f64ebc988455d988bb75',
            url='https://gforge.inria.fr/frs/download.php/file/37758/SimGrid-3.21.tar.gz')
    version('3.20', 'df65463394f0f4a8e02758bf558eeb3f',
            url='https://gforge.inria.fr/frs/download.php/file/37602/SimGrid-3.20.tar.gz')
    version('3.19', 'e6e1a56685505595617dacd5e617868e',
            url='https://gforge.inria.fr/frs/download.php/file/37452/SimGrid-3.19.tar.gz')
    version('3.18', 'a3f457f70eb9ef095c275672b21247f4',
            url='https://gforge.inria.fr/frs/download.php/file/37294/SimGrid-3.18.tar.gz')
    version('3.17', '0abf5a7265931bf0ce269399f26b6fc1',
            url='https://gforge.inria.fr/frs/download.php/file/37148/SimGrid-3.17.tar.gz')
    version('3.16', '7a2529d8769dd7ae1b088d7bcc6fcc14',
            url='https://gforge.inria.fr/frs/download.php/file/36900/SimGrid-3.16.tar.gz')
    version('3.15', 'e196d30e80350dce8cd41b0af468c4fc',
            url='https://gforge.inria.fr/frs/download.php/file/36621/SimGrid-3.15.tar.gz')
    version('3.14.159', 'a23be064ceb59714055199167efa0828',
            url='http://gforge.inria.fr/frs/download.php/file/36384/SimGrid-3.14.159.tar.gz')
    version('3.13', '8ace1684972a01429d5f1c5db8966709',
            url='http://gforge.inria.fr/frs/download.php/file/35817/SimGrid-3.13.tar.gz')
    version('3.12', 'd73faaf81d7a9eb0d309cfd72532c5f1',
            url='http://gforge.inria.fr/frs/download.php/file/35215/SimGrid-3.12.tar.gz')
    version('3.11', '358ed81042bd283348604eb1beb80224',
            url='http://gforge.inria.fr/frs/download.php/file/33683/SimGrid-3.11.tar.gz')
    version('git', branch='master')

    variant('doc', default=False, description='Build documentation')
    variant('smpi', default=True, description='SMPI provides MPI')
    variant('examples', default=False, description='Install examples')
    variant('mc', default=False, description='Model checker')

    # does not build correctly with some old compilers -> rely on packages
    depends_on('boost')

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
