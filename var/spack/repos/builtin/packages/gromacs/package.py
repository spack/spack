# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gromacs(CMakePackage):
    """GROMACS (GROningen MAchine for Chemical Simulations) is a molecular
    dynamics package primarily designed for simulations of proteins, lipids
    and nucleic acids. It was originally developed in the Biophysical
    Chemistry department of University of Groningen, and is now maintained
    by contributors in universities and research centers across the world.

    GROMACS is one of the fastest and most popular software packages
    available and can run on CPUs as well as GPUs. It is free, open source
    released under the GNU General Public License. Starting from version 4.6,
    GROMACS is released under the GNU Lesser General Public License.
    """

    homepage = 'http://www.gromacs.org'
    url      = 'http://ftp.gromacs.org/gromacs/gromacs-5.1.2.tar.gz'
    git      = 'https://github.com/gromacs/gromacs.git'

    version('develop', branch='master')
    version('2018.4', sha256='6f2ee458c730994a8549d6b4f601ecfc9432731462f8bd4ffa35d330d9aaa891')
    version('2018.3', sha256='4423a49224972969c52af7b1f151579cea6ab52148d8d7cbae28c183520aa291')
    version('2018.2', '7087462bb08393aec4ce3192fa4cd8df')
    version('2018.1', '7ee393fa3c6b7ae351d47eae2adf980e')
    version('2018',   '6467ffb1575b8271548a13abfba6374c')
    version('2016.5', 'f41807e5b2911ccb547a3fd11f105d47')
    version('2016.4', '19c8b5c85f3ec62df79d2249a3c272f8')
    version('2016.3', 'e9e3a41bd123b52fbcc6b32d09f8202b')
    version('5.1.5',  '831fe741bcd9f1612155dffc919885f2')
    version('5.1.4',  'ba2e34d59b3982603b4935d650c08040')
    version('5.1.2',  '614d0be372f1a6f1f36382b7a6fcab98')

    variant('mpi', default=True, description='Activate MPI support')
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant(
        'double', default=False,
        description='Produces a double precision version of the executables')
    variant('plumed', default=False, description='Enable PLUMED support')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel',
                    'Reference', 'RelWithAssert', 'Profile'))

    depends_on('mpi', when='+mpi')
    depends_on('plumed+mpi', when='+plumed+mpi')
    depends_on('plumed~mpi', when='+plumed~mpi')
    depends_on('fftw')
    depends_on('cmake@2.8.8:3.9.99', type='build')
    depends_on('cmake@3.4.3:3.9.99', type='build', when='@2018:')
    depends_on('cuda', when='+cuda')

    def patch(self):
        if '+plumed' in self.spec:
            self.spec['plumed'].package.apply_patch(self)

    def cmake_args(self):

        options = []

        if '+mpi' in self.spec:
            options.append('-DGMX_MPI:BOOL=ON')

        if '+double' in self.spec:
            options.append('-DGMX_DOUBLE:BOOL=ON')

        if '~shared' in self.spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=OFF')

        if '+cuda' in self.spec:
            options.append('-DGMX_GPU:BOOL=ON')
            options.append('-DCUDA_TOOLKIT_ROOT_DIR:STRING=' +
                           self.spec['cuda'].prefix)

        return options
