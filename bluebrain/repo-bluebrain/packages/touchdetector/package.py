##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Touchdetector(CMakePackage):
    """Detects touches between cells
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/touchdetector"
    url      = "git@bbpgitlab.epfl.ch:hpc/touchdetector.git"
    git      = "git@bbpgitlab.epfl.ch:hpc/touchdetector.git"

    generator = "Ninja"

    version('develop', submodules=True)
    version('5.6.1', tag='5.6.1', submodules=True)
    version('5.6.0', tag='5.6.0', submodules=True)
    version('5.5.1', tag='5.5.1', submodules=True)
    version('5.5.0', tag='5.5.0', submodules=True)
    version('5.4.0', tag='5.4.0', submodules=True)
    version('5.3.4', tag='5.3.4', submodules=True)
    version('5.3.3', tag='5.3.3', submodules=True)
    version('5.3.2', tag='5.3.2', submodules=True)
    version('5.3.1', tag='5.3.1', submodules=True)
    version('5.3.0', tag='5.3.0', submodules=True)
    version('5.2.0', tag='5.2.0', submodules=True)
    version('5.1.0', tag='5.1.0', submodules=True)
    version('5.0.1', tag='5.0.1', submodules=True)
    version('5.0.0', tag='5.0.0', submodules=True)
    version('4.4.2', tag='4.4.2', submodules=True)
    version('4.4.1', tag='4.4.1', submodules=True)
    version('4.3.3', tag='4.3.3', submodules=True)

    variant('openmp', default=False, description='Enables OpenMP support')

    depends_on('cmake', type='build')
    depends_on('ninja', type='build')
    depends_on('catch2', when='@5.0.2:')
    depends_on('eigen', when='@4.5:')
    depends_on('fmt@:5.999', when='@4.5:')
    depends_on('morpho-kit', when='@5.2:')
    depends_on('mpi')
    depends_on('pugixml', when='@4.5:')
    depends_on('random123', when='@5.3.3:')
    depends_on('range-v3@:0.4', when='@5.0.2:5.3.2')
    depends_on('range-v3@:0.10', when='@5.3.3:')
    depends_on('libsonata@0.1.9:', when='@5.6.0:')
    depends_on('nlohmann-json', when='@5.3.3:')
    depends_on('intel-oneapi-tbb', when='@develop')

    # Old dependencies
    depends_on('hpctools~openmp', when='~openmp@:4.4')
    depends_on('hpctools+openmp', when='+openmp@:4.4')
    depends_on('libxml2', when='@:4.4')
    depends_on('zlib', when='@:4.4')

    depends_on('morphio@2.0.8:', when='@4.5:5.1')
    depends_on('mvdtool@2.1.0:', when='@5.1.1:5.5.999')
    depends_on('mvdtool@1.5.1:2.0.0', when='@4.5:5.1')

    depends_on('highfive+mpi', when='@5.3.0:5.6.1')
    depends_on('boost@1.50:', when='@:5.6.1')

    patch("no-wall.patch", when='@5:5.4.999')
    patch("fix-cmake.patch", when='@5.6.1')

    def patch(self):
        if self.spec.satisfies('@5.6.1'):
            filter_file(r'(int messageLength) = -1;$',
                        r'\1 = 0;',
                        'touchdetector/DistributedTouchDetector.cxx')
        elif self.spec.satisfies('@develop'):
            filter_file(
                r'-Werror',
                '-Werror -Wno-error=stringop-overflow',
                'touchdetector/CMakeLists.txt'
            )

    def cmake_args(self):
        args = [
            '-DUSE_OPENMP:BOOL={0}'.format('+openmp' in self.spec),
            '-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx),
        ]
        return args
