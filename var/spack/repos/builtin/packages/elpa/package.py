# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Elpa(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Eigenvalue solvers for Petaflop-Applications (ELPA)"""

    homepage = 'https://elpa.mpcdf.mpg.de/'
    url = 'https://elpa.mpcdf.mpg.de/software/tarball-archive/Releases/2015.11.001/elpa-2015.11.001.tar.gz'

    version('2021.05.001', sha256='a4f1a4e3964f2473a5f8177f2091a9da5c6b5ef9280b8272dfefcbc3aad44d41')
    version('2020.05.001', sha256='66ff1cf332ce1c82075dc7b5587ae72511d2bcb3a45322c94af6b01996439ce5')
    version('2019.11.001', sha256='10374a8f042e23c7e1094230f7e2993b6f3580908a213dbdf089792d05aff357')
    version('2019.05.002', sha256='d2eab5e5d74f53601220b00d18185670da8c00c13e1c1559ecfb0cd7cb2c4e8d')
    version('2018.11.001', sha256='cc27fe8ba46ce6e6faa8aea02c8c9983052f8e73a00cfea38abf7613cb1e1b16')
    version('2018.05.001.rc1', sha256='598c01da20600a4514ea4d503b93e977ac0367e797cab7a7c1b0e0e3e86490db')
    version('2017.11.001', sha256='59f99c3abe2190fac0db8a301d0b9581ee134f438669dbc92551a54f6f861820')
    version('2017.05.003', sha256='bccd49ce35a323bd734b17642aed8f2588fea4cc78ee8133d88554753bc3bf1b')
    version('2017.05.002', sha256='568b71024c094d667b5cbb23045ad197ed5434071152ac608dae490ace5eb0aa')
    version('2017.05.001', sha256='28f7edad60984d93da299016ad33571dc6db1cdc9fab0ceaef05dc07de2c7dfd')
    version('2016.11.001.pre', sha256='69b67f0f6faaa2b3b5fd848127b632be32771636d2ad04583c5269d550956f92')
    version('2016.05.004', sha256='08c59dc9da458bab856f489d779152e5506e04f0d4b8d6dcf114ca5fbbe46c58')
    version('2016.05.003', sha256='c8da50c987351514e61491e14390cdea4bdbf5b09045261991876ed5b433fca4')
    version('2015.11.001', sha256='c0761a92a31c08a4009c9688c85fc3fc8fde9b6ce05e514c3e1587cf045e9eba')

    variant('openmp', default=True, description='Activates OpenMP support')
    variant('mpi', default=True, description='Activates MPI support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+mpi')
    depends_on('rocblas', when='+rocm')
    depends_on('libtool', type='build')
    depends_on('python@:2', type='build', when='@:2020.05.001')
    depends_on('python@3:', type='build', when='@2020.11.001:')

    patch('python_shebang.patch', when='@:2020.05.001')

    # fails to build due to broken type-bound procedures in OMP parallel regions
    conflicts('+openmp', when='@2021.05.001: %gcc@:7',
              msg='ELPA-2021.05.001+ requires GCC-8+ for OpenMP support')
    conflicts('+rocm', when='@:2020',
              msg='ROCm support was introduced in ELPA 2021.05.001')
    conflicts('+mpi', when='+rocm',
              msg='ROCm support and MPI are not yet compatible')

    def url_for_version(self, version):
        return ('https://elpa.mpcdf.mpg.de/software/tarball-archive/Releases/{0}/elpa-{0}.tar.gz'
                .format(str(version)))

    # override default implementation which returns static lib
    @property
    def libs(self):
        libname = 'libelpa_openmp' if '+openmp' in self.spec else 'libelpa'
        return find_libraries(
            libname, root=self.prefix, shared=True, recursive=True
        )

    @property
    def headers(self):
        suffix = '_openmp' if self.spec.satisfies('+openmp') else ''
        incdir = os.path.join(
            self.spec.prefix.include,
            'elpa{suffix}-{version!s}'.format(
                suffix=suffix, version=self.spec.version))

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    build_directory = 'spack-build'
    parallel = False

    def configure_args(self):
        spec = self.spec
        options = []

        options += self.with_or_without('mpi')

        # TODO: --disable-sse-assembly, --enable-sparc64, --enable-neon-arch64
        simd_features = ['vsx', 'sse', 'avx', 'avx2', 'avx512',
                         'sve128', 'sve256', 'sve512']

        for feature in simd_features:
            msg = '--enable-{0}' if feature in spec.target else '--disable-{0}'
            options.append(msg.format(feature))

        if spec.target.family == 'aarch64':
            options.append('--disable-sse-assembly')

        if '%aocc' in spec:
            options.append('--disable-shared')
            options.append('--enable-static')

        # If no features are found, enable the generic ones
        if not any(f in spec.target for f in simd_features):
            options.append('--enable-generic')

        if self.compiler.name == "gcc":
            gcc_options = []
            gfortran_options = ['-ffree-line-length-none']

            if self.compiler.version >= Version("10.0.0") \
               and spec.version <= Version("2019.11.001"):
                gfortran_options.append('-fallow-argument-mismatch')

            space_separator = ' '
            options.extend([
                'CFLAGS=' + space_separator.join(gcc_options),
                'FCFLAGS=' + space_separator.join(gfortran_options),
            ])

        if '%aocc' in spec:
            options.extend([
                'FCFLAGS=-O3',
                'CFLAGS=-O3'
            ])

        cuda_flag = 'nvidia-gpu' if '@2021.05.001:' in self.spec else 'gpu'
        if '+cuda' in spec:
            prefix = spec['cuda'].prefix
            options.append('--enable-{0}'.format(cuda_flag))
            options.append('--with-cuda-path={0}'.format(prefix))
            options.append('--with-cuda-sdk-path={0}'.format(prefix))

            cuda_arch = spec.variants['cuda_arch'].value[0]

            if cuda_arch != 'none':
                options.append('--with-{0}-compute-capability=sm_{1}'.
                               format(cuda_flag.upper(), cuda_arch))
        else:
            options.append('--disable-{0}'.format(cuda_flag))

        if '+rocm' in spec:
            options.append('--enable-amd-gpu')
            options.append('CXX={0}'.format(self.spec['hip'].hipcc))
        elif '@2021.05.001:' in self.spec:
            options.append('--disable-amd-gpu')

        options += self.enable_or_disable('openmp')

        options += [
            'LDFLAGS={0}'.format(spec['lapack'].libs.search_flags),
            'LIBS={0} {1}'.format(
                spec['lapack'].libs.link_flags, spec['blas'].libs.link_flags)]

        if '+mpi' in self.spec:
            options += [
                'CC={0}'.format(spec['mpi'].mpicc),
                'CXX={0}'.format(spec['mpi'].mpicxx),
                'FC={0}'.format(spec['mpi'].mpifc),
                'SCALAPACK_LDFLAGS={0}'.format(spec['scalapack'].libs.joined())
            ]

        options.append('--disable-silent-rules')

        return options
