# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rmgdft(CMakePackage):
    """RMGDFT is a high performance real-space density functional code
       designed for large scale electronic structure calculations."""

    homepage = "http://www.rmgdft.org/"
    git      = "https://github.com/RMGDFT/rmgdft.git"
    maintainers = ['elbriggs']
    tags = ['ecp', 'ecp-apps']
    version('master', branch='master')
    version('4.2.2', tag='v4.2.2')
    version('4.2.1', tag='v4.2.1')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    variant('qmcpack', default=True,
            description='Build with qmcpack interface.')

    variant('local_orbitals', default=True,
            description='Build O(N) variant.')

    # Normally we want this but some compilers (e.g. IBM) are
    # very slow when this is on so provide the option to disable
    variant('internal_pp', default=True,
            description='Include built-in pseudopotentials. Normally '
                        'enabled but some compilers are slow when '
                        'this is on so provide a disable option.')

    # RMGDFT 4.0.0 or later requires compiler support for C++14
    compiler_warning = 'RMGDFT 4.0.0 or later requires a ' \
                       'compiler with support for C++14'
    conflicts('%gcc@:4', when='@3.6.0:', msg=compiler_warning)
    conflicts('%intel@:17', when='@3.6.0:', msg=compiler_warning)
    conflicts('%pgi@:17', when='@3.6.0:', msg=compiler_warning)
    conflicts('%llvm@:3.4', when='@3.6.0:', msg=compiler_warning)

    depends_on('cmake', type='build')
    depends_on('boost@1.66.0:')
    depends_on('fftw-api@3')
    depends_on('mpi')
    depends_on('hdf5')

    # RMG is a hybrid MPI/threads code and performance is
    # highly dependent on the threading model of the blas
    # libraries. Openblas-openmp is known to work well
    # so if spack yields a non-performant build you can
    # try to adjust your system config to use it.
    depends_on('blas')
    conflicts('^atlas',
              msg='The atlas threading model is incompatible with RMG')

    @property
    def build_targets(self):
        spec = self.spec
        targets = ['rmg-cpu']
        if '+local_orbitals' in spec:
            targets.append('rmg-on-cpu')
        return targets

    def cmake_args(self):
        spec = self.spec
        args = []
        if '+qmcpack' in spec:
            args.append('-DQMCPACK=1')
        else:
            args.append('-DQMCPACK=0')
        if '+internal_pp' in spec:
            args.append('-DUSE_INTERNAL_PSEUDOPOTENTIALS=1')
        else:
            args.append('-DUSE_INTERNAL_PSEUDOPOTENTIALS=0')
        return args

    def install(self, spec, prefix):

        # create top-level directories
        mkdirp(prefix.bin)
        mkdirp(prefix.share.tests.RMG)

        with working_dir(self.build_directory):
            install('rmg-cpu', prefix.bin)
            if '+local_orbitals' in spec:
                install('rmg-on-cpu', prefix.bin)

        # install tests
        with working_dir(self.build_directory):
            install_tree('tests/RMG', prefix.share.tests.RMG)
