# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Alps(CMakePackage):
    """Algorithms for Physics Simulations

    Keywords: Condensed Matter Physics, Computational Physics
    """

    homepage = "https://alps.comp-phys.org"
    url      = "http://alps.comp-phys.org/static/software/releases/alps-2.3.0-src.tar.gz"

    version('2.3.0', sha256='e64208d1e5acdd6f569277413c4867e1fa366cf4a224570eacbf1e9939fca2d2')

    # http://alps.comp-phys.org/mediawiki/index.php/Building_ALPS_from_source
    # https://github.com/easybuilders/easybuild-easyconfigs/tree/master/easybuild/easyconfigs/a/ALPS
    depends_on('boost@1.63.0 +mpi +numpy +python')
    depends_on('fftw')
    depends_on('hdf5@1.8.17~mpi+hl')
    depends_on('openblas')
    # build fails for latest python@3.7
    depends_on('python@:3.6.99', type=('build', 'link', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))

    conflicts('%gcc@7:')

    root_cmakelists_dir = 'alps'

    patch('mpi.patch')

    def cmake_args(self):
        args = []
        args.append('Boost_ROOT_DIR=' + self.spec['boost'].prefix)
        args.append("-DCMAKE_CXX_FLAGS=-std=c++03 ")
        return args
