# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import os
import os.path

import spack.util.environment
from spack.package import *


class Cp2k(MakefilePackage, CudaPackage):
    """CP2K is a quantum chemistry and solid state physics software package
    that can perform atomistic simulations of solid state, liquid, molecular,
    periodic, material, crystal, and biological systems
    """
    homepage = 'https://www.cp2k.org'
    url = 'https://github.com/cp2k/cp2k/releases/download/v3.0.0/cp2k-3.0.tar.bz2'
    git = 'https://github.com/cp2k/cp2k.git'
    list_url = 'https://github.com/cp2k/cp2k/releases'

    maintainers = ['dev-zero']

    version('9.1', sha256='fedb4c684a98ad857cd49b69a3ae51a73f85a9c36e9cb63e3b02320c74454ce6')
    version('8.2', sha256='2e24768720efed1a5a4a58e83e2aca502cd8b95544c21695eb0de71ed652f20a')
    version('8.1', sha256='7f37aead120730234a60b2989d0547ae5e5498d93b1e9b5eb548c041ee8e7772')
    version('7.1', sha256='ccd711a09a426145440e666310dd01cc5772ab103493c4ae6a3470898cd0addb')
    version('6.1', sha256='af803558e0a6b9e9d9ce8a3ab955ba32bacd179922455424e061c82c9fefa34b')
    version('5.1', sha256='e23613b593354fa82e0b8410e17d94c607a0b8c6d9b5d843528403ab09904412')
    version('4.1', sha256='4a3e4a101d8a35ebd80a9e9ecb02697fb8256364f1eccdbe4e5a85d31fe21343')
    version('3.0', sha256='1acfacef643141045b7cbade7006f9b7538476d861eeecd9658c9e468dc61151')
    version('master', submodules=True)

    variant('mpi', default=True, description='Enable MPI support')
    variant('openmp', default=True, description='Enable OpenMP support')
    variant('smm', default='libxsmm', values=('libxsmm', 'libsmm', 'blas'),
            description='Library for small matrix multiplications')
    variant('plumed', default=False, description='Enable PLUMED support')
    variant('libint', default=True,
            description='Use libint, required for HFX (and possibly others)')
    variant('libxc', default=True,
            description='Support additional functionals via libxc')
    variant('pexsi', default=False,
            description=('Enable the alternative PEXSI method'
                         'for density matrix evaluation'))
    variant('elpa', default=False,
            description='Enable optimised diagonalisation routines from ELPA')
    variant('sirius', default=False,
            description=('Enable planewave electronic structure'
                         ' calculations via SIRIUS'))
    variant('cosma', default=False, description='Use COSMA for p?gemm')
    variant('libvori', default=False,
            description=('Enable support for Voronoi integration'
                         ' and BQB compression'))
    variant('spglib', default=False, description='Enable support for spglib')

    with when('+cuda'):
        variant('cuda_arch_35_k20x', default=False,
                description=('CP2K (resp. DBCSR) has specific parameter sets for'
                             ' different GPU models. Enable this when building'
                             ' with cuda_arch=35 for a K20x instead of a K40'))
        variant('cuda_fft', default=False,
                description=('Use CUDA also for FFTs in the PW part of CP2K'))
        variant('cuda_blas', default=False, when='@:7',  # req in CP2K v8+
                description=('Use CUBLAS for general matrix operations in DBCSR'))

    HFX_LMAX_RANGE = range(4, 8)

    variant('lmax',
            description='Maximum supported angular momentum (HFX and others)',
            default='5',
            values=[str(x) for x in HFX_LMAX_RANGE],
            multi=False)

    depends_on('python', type='build')
    depends_on('python@3:', when='@8:', type='build')

    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api@3')

    # Force openmp propagation on some providers of blas / fftw-api
    with when('+openmp'):
        depends_on('fftw+openmp', when='^fftw')
        depends_on('amdfftw+openmp', when='^amdfftw')
        depends_on('cray-fftw+openmp', when='^cray-fftw')
        depends_on('openblas threads=openmp', when='^openblas')
        # The Cray compiler wrappers will automatically add libsci_mp with
        # -fopenmp. Since CP2K unconditionally links blas/lapack/scalapack
        # we have to be consistent.
        depends_on('cray-libsci+openmp', when='^cray-libsci')

    with when('smm=libxsmm'):
        depends_on('libxsmm@1.17:~header-only', when='@9.1:')
        # require libxsmm-1.11+ since 1.10 can leak file descriptors in Fortran
        depends_on('libxsmm@1.11:~header-only', when="@:8.9")
        # use pkg-config (support added in libxsmm-1.10) to link to libxsmm
        depends_on('pkgconfig', type='build')
        # please set variants: smm=blas by configuring packages.yaml or install
        # cp2k with option smm=blas on aarch64
        conflicts('target=aarch64:', msg='libxsmm is not available on arm')

    with when('+libint'):
        # ... and in CP2K 7.0+ for linking to libint2
        depends_on('pkgconfig', type='build', when='@7.0:')
        # libint & libxc are always statically linked
        depends_on('libint@1.1.4:1.2', when='@3.0:6.9')
        for lmax in HFX_LMAX_RANGE:
            # libint2 can be linked dynamically again
            depends_on('libint@2.6.0:+fortran tune=cp2k-lmax-{0}'.format(lmax),
                       when='@7.0: lmax={0}'.format(lmax))

    with when('+libxc'):
        depends_on('pkgconfig', type='build', when='@7.0:')
        depends_on('libxc@2.2.2:3', when='@:5', type='build')
        depends_on('libxc@4.0.3:4', when='@6.0:6.9', type='build')
        depends_on('libxc@4.0.3:4', when='@7.0:8.1')
        depends_on('libxc@5.1.3:5.1', when='@8.2:8')
        depends_on('libxc@5.1.7:5.1', when='@9:')

    with when('+mpi'):
        depends_on('mpi@2:')
        depends_on('scalapack')

    with when('+cosma'):
        depends_on('cosma+scalapack')
        depends_on('cosma@2.5.1:', when='@9:')
        depends_on('cosma+cuda', when='+cuda')
        conflicts('~mpi')
        # COSMA support was introduced in 8+
        conflicts('@:7')

    with when('+elpa'):
        conflicts('~mpi', msg='elpa requires MPI')
        depends_on('elpa+openmp', when='+openmp')
        depends_on('elpa~openmp', when='~openmp')
        depends_on('elpa@2011.12:2016.13', when='@:5')
        depends_on('elpa@2011.12:2017.11', when='@6.0:6')
        depends_on('elpa@2018.05:2020.11.001', when='@7.0:8.2')
        depends_on('elpa@2021.05:', when='@8.3:')
        depends_on('elpa@2021.11.001:', when='@9.1:')

    with when('+plumed'):
        depends_on('plumed+shared')
        depends_on('plumed+mpi', when='+mpi')
        depends_on('plumed~mpi', when='~mpi')

    # while we link statically against PEXSI, its own deps may be linked in
    # dynamically, therefore can't set this as pure build-type dependency.
    with when('+pexsi'):
        conflicts('~mpi', msg='pexsi requires MPI')
        depends_on('pexsi+fortran@0.9.0:0.9', when='@:4')
        depends_on('pexsi+fortran@0.10.0:', when='@5.0:')

    # only OpenMP should be consistently used, all other common things
    # like ELPA, SCALAPACK are independent and Spack will ensure that
    # a consistent/compatible combination is pulled into the dependency graph.
    with when('+sirius'):
        depends_on('sirius+fortran+shared')
        depends_on('sirius+openmp', when='+openmp')
        depends_on('sirius~openmp', when='~openmp')
        depends_on('sirius@:6', when='@:7')
        depends_on('sirius@7.0.0:7.0', when='@8:8.2')
        depends_on('sirius@7.2', when='@8.3:8.9')
        depends_on('sirius@7.3:', when='@9.1')
        conflicts('~mpi')
        # sirius support was introduced in 7+
        conflicts('@:6')

    with when('+libvori'):
        depends_on('libvori@201219:', when='@8.1', type='build')
        depends_on('libvori@210412:', when='@8.2:', type='build')
        # libvori support was introduced in 8+
        conflicts('@:7')

    # the bundled libcusmm uses numpy in the parameter prediction (v7+)
    # which is written using Python 3
    depends_on('py-numpy', when='@7:+cuda', type='build')
    depends_on('python@3.6:', when='@7:+cuda', type='build')

    depends_on('spglib', when='+spglib')

    # Apparently cp2k@4.1 needs an "experimental" version of libwannier.a
    # which is only available contacting the developer directly. See INSTALL
    # in the stage of cp2k@4.1
    depends_on('wannier90', when='@3.0+mpi', type='build')

    # CP2K needs compiler specific compilation flags, e.g. optflags
    conflicts('%apple-clang')
    conflicts('%clang')
    conflicts('%nag')

    conflicts('~openmp', when='@8:', msg='Building without OpenMP is not supported in CP2K 8+')

    # We only support specific cuda_archs for which we have parameter files
    # for optimal kernels. Note that we don't override the cuda_archs property
    # from the parent class, since the parent class defines constraints for all
    # versions. Instead just mark all unsupported cuda archs as conflicting.
    dbcsr_cuda_archs = ('35', '37', '60', '70')
    cuda_msg = 'cp2k only supports cuda_arch {0}'.format(dbcsr_cuda_archs)

    for arch in CudaPackage.cuda_arch_values:
        if arch not in dbcsr_cuda_archs:
            conflicts('+cuda', when='cuda_arch={0}'.format(arch), msg=cuda_msg)

    conflicts('+cuda', when='cuda_arch=none', msg=cuda_msg)

    # Fix 2- and 3-center integral calls to libint
    patch("https://github.com/cp2k/cp2k/commit/5eaf864ed2bd21fb1b05a9173bb77a815ad4deda.patch?full_index=1",
          sha256="3617abb877812c4b933f601438c70f95e21c6161bea177277b1d4125fd1c0bf9",
          when="@8.2")

    @property
    def makefile_architecture(self):
        return '{0.architecture}-{0.compiler.name}'.format(self.spec)

    @property
    def makefile_version(self):
        return '{prefix}{suffix}'.format(
            prefix='p' if '+mpi' in self.spec else 's',
            suffix='smp' if '+openmp' in self.spec else 'opt'
        )

    @property
    def makefile(self):
        makefile_basename = '.'.join([
            self.makefile_architecture, self.makefile_version
        ])
        return join_path('arch', makefile_basename)

    @property
    def archive_files(self):
        return [join_path(self.stage.source_path, self.makefile)]

    def edit(self, spec, prefix):
        pkgconf = which('pkg-config')

        if '^fftw' in spec:
            fftw = spec['fftw:openmp' if '+openmp' in spec else 'fftw']
            fftw_header_dir = fftw.headers.directories[0]
        elif '^amdfftw' in spec:
            fftw = spec['amdfftw:openmp' if '+openmp' in spec else 'amdfftw']
            fftw_header_dir = fftw.headers.directories[0]
        elif '^intel-mkl' in spec:
            fftw = spec['intel-mkl']
            fftw_header_dir = fftw.headers.directories[0] + '/fftw'
        elif '^intel-oneapi-mkl' in spec:
            fftw = spec['intel-oneapi-mkl']
            fftw_header_dir = fftw.headers.directories[0] + '/fftw'
        elif '^intel-parallel-studio+mkl' in spec:
            fftw = spec['intel-parallel-studio']
            fftw_header_dir = '<NOTFOUND>'
            for incdir in [join_path(f, 'fftw')
                           for f in fftw.headers.directories]:
                if os.path.exists(incdir):
                    fftw_header_dir = incdir
                    break
        elif '^cray-fftw' in spec:
            fftw = spec['cray-fftw']
            fftw_header_dir = fftw.headers.directories[0]

        optimization_flags = {
            'gcc': [
                '-O2',
                '-funroll-loops',
                '-ftree-vectorize',
            ],
            'intel': ['-O2', '-pc64', '-unroll', ],
            'pgi': ['-fast'],
            'nvhpc': ['-fast'],
            'cce': ['-O2'],
            'xl': ['-O3'],
            'aocc': ['-O1'],
        }

        dflags = ['-DNDEBUG']
        cppflags = [
            '-D__FFTW3',
            '-I{0}'.format(fftw_header_dir),
        ]

        if '^mpi@3:' in spec:
            cppflags.append('-D__MPI_VERSION=3')
        elif '^mpi@2:' in spec:
            cppflags.append('-D__MPI_VERSION=2')

        cflags = optimization_flags[self.spec.compiler.name][:]
        cxxflags = optimization_flags[self.spec.compiler.name][:]
        fcflags = optimization_flags[self.spec.compiler.name][:]
        nvflags = ['-O3']
        ldflags = []
        libs = []
        gpuver = ''

        if '%intel' in spec:
            cflags.append('-fp-model precise')
            cxxflags.append('-fp-model precise')
            fcflags += [
                '-fp-model precise',
                '-heap-arrays 64',
                '-g',
                '-traceback',
            ]
        elif '%gcc' in spec:
            fcflags += [
                '-ffree-form',
                '-ffree-line-length-none',
                '-ggdb',  # make sure we get proper Fortran backtraces
            ]
        elif '%aocc' in spec:
            fcflags += [
                '-ffree-form',
                '-Mbackslash',
            ]
        elif '%pgi' in spec or '%nvhpc' in spec:
            fcflags += ['-Mfreeform', '-Mextend']
        elif '%cce' in spec:
            fcflags += ['-emf', '-ffree', '-hflex_mp=strict']
        elif '%xl' in spec:
            fcflags += ['-qpreprocess', '-qstrict', '-q64']
            ldflags += ['-Wl,--allow-multiple-definition']

        if '%gcc@10: +mpi' in spec and spec['mpi'].name in ['mpich', 'cray-mpich']:
            fcflags += ['-fallow-argument-mismatch']  # https://github.com/pmodels/mpich/issues/4300

        if '+openmp' in spec:
            cflags.append(self.compiler.openmp_flag)
            cxxflags.append(self.compiler.openmp_flag)
            fcflags.append(self.compiler.openmp_flag)
            ldflags.append(self.compiler.openmp_flag)
            nvflags.append('-Xcompiler="{0}"'.format(
                self.compiler.openmp_flag))
        elif '%cce' in spec:  # Cray enables OpenMP by default
            cflags   += ['-hnoomp']
            cxxflags += ['-hnoomp']
            fcflags  += ['-hnoomp']
            ldflags  += ['-hnoomp']

        if '@7:' in spec:  # recent versions of CP2K use C++14 CUDA code
            cxxflags.append(self.compiler.cxx14_flag)
            nvflags.append(self.compiler.cxx14_flag)

        ldflags.append(fftw.libs.search_flags)

        if 'superlu-dist@4.3' in spec:
            ldflags.insert(0, '-Wl,--allow-multiple-definition')

        if '+plumed' in self.spec:
            dflags.extend(['-D__PLUMED2'])
            cppflags.extend(['-D__PLUMED2'])
            libs.extend([
                join_path(self.spec['plumed'].prefix.lib,
                          'libplumed.{0}'.format(dso_suffix))
            ])

        cc = spack_cc if '~mpi' in spec else spec['mpi'].mpicc
        cxx = spack_cxx if '~mpi' in spec else spec['mpi'].mpicxx
        fc = spack_fc if '~mpi' in spec else spec['mpi'].mpifc

        # Intel
        if '%intel' in spec:
            cppflags.extend([
                '-D__INTEL',
                '-D__HAS_ISO_C_BINDING',
                '-D__USE_CP2K_TRACE',
            ])
            fcflags.extend([
                '-diag-disable 8290,8291,10010,10212,11060',
                '-free',
                '-fpp'
            ])

        # FFTW, LAPACK, BLAS
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs
        ldflags.append((lapack + blas).search_flags)
        libs.extend([str(x) for x in (fftw.libs, lapack, blas)])

        if any(p in spec for p in ('^intel-mkl',
                                   '^intel-parallel-studio+mkl',
                                   '^intel-oneapi-mkl')):
            cppflags += ['-D__MKL']
        elif '^accelerate' in spec:
            cppflags += ['-D__ACCELERATE']

        if '+cosma' in spec:
            # add before ScaLAPACK to override the p?gemm symbols
            cosma = spec['cosma'].libs
            ldflags.append(cosma.search_flags)
            libs.extend(cosma)

        # MPI
        if '+mpi' in spec:
            cppflags.extend([
                '-D__parallel',
                '-D__SCALAPACK'
            ])

            if '^intel-oneapi-mpi' in spec:
                mpi = [join_path(
                       spec['intel-oneapi-mpi'].libs.directories[0],
                       'libmpi.so')]
            else:
                mpi = spec['mpi:cxx'].libs

            # while intel-mkl has a mpi variant and adds the scalapack
            # libs to its libs, intel-oneapi-mkl does not.
            if '^intel-oneapi-mkl' in spec:
                mpi_impl = 'openmpi' if '^openmpi' in spec else 'intelmpi'
                scalapack = [
                    join_path(
                        spec['intel-oneapi-mkl'].libs.directories[0],
                        'libmkl_scalapack_lp64.so'),
                    join_path(
                        spec['intel-oneapi-mkl'].libs.directories[0],
                        'libmkl_blacs_{0}_lp64.so'.format(mpi_impl)
                    )
                ]
            else:
                scalapack = spec['scalapack'].libs
                ldflags.append(scalapack.search_flags)

            libs.extend(scalapack)
            libs.extend(mpi)
            libs.extend(self.compiler.stdcxx_libs)

            if 'wannier90' in spec:
                cppflags.append('-D__WANNIER90')
                wannier = join_path(
                    spec['wannier90'].libs.directories[0], 'libwannier.a'
                )
                libs.append(wannier)

        if '+libint' in spec:
            cppflags += ['-D__LIBINT']

            if '@:6.9' in spec:
                cppflags += [
                    '-D__LIBINT_MAX_AM=6',
                    '-D__LIBDERIV_MAX_AM1=5',
                ]

                # libint-1.x.y has to be linked statically to work around
                # inconsistencies in its Fortran interface definition
                # (short-int vs int) which otherwise causes segfaults at
                # runtime due to wrong offsets into the shared library
                # symbols.
                libs.extend([
                    join_path(
                        spec['libint'].libs.directories[0], 'libderiv.a'),
                    join_path(
                        spec['libint'].libs.directories[0], 'libint.a'),
                ])
            else:
                fcflags += pkgconf('--cflags', 'libint2', output=str).split()
                libs += pkgconf('--libs', 'libint2', output=str).split()

        if '+libxc' in spec:
            cppflags += ['-D__LIBXC']

            if '@:6.9' in spec:
                libxc = spec['libxc:fortran,static']
                cppflags += [libxc.headers.cpp_flags]
                ldflags.append(libxc.libs.search_flags)
                libs.append(str(libxc.libs))
            else:
                fcflags += pkgconf('--cflags', 'libxcf03', output=str).split()
                # some Fortran functions seem to be direct wrappers of the
                # C functions such that we get a direct dependency on them,
                # requiring `-lxc` to be present in addition to `-lxcf03`
                libs += pkgconf('--libs', 'libxcf03', 'libxc', output=str).split()

        if '+pexsi' in spec:
            cppflags.append('-D__LIBPEXSI')
            fcflags.append('-I' + join_path(
                spec['pexsi'].prefix, 'fortran'))
            libs.extend([
                join_path(spec['pexsi'].libs.directories[0], 'libpexsi.a'),
                join_path(spec['superlu-dist'].libs.directories[0],
                          'libsuperlu_dist.a'),
                join_path(
                    spec['parmetis'].libs.directories[0],
                    'libparmetis.{0}'.format(dso_suffix)
                ),
                join_path(
                    spec['metis'].libs.directories[0],
                    'libmetis.{0}'.format(dso_suffix)
                ),
            ])

        if '+elpa' in spec:
            elpa = spec['elpa']
            elpa_suffix = '_openmp' if '+openmp' in elpa else ''
            elpa_incdir = elpa.headers.directories[0]

            fcflags += ['-I{0}'.format(join_path(elpa_incdir, 'modules'))]

            # Currently AOCC support only static libraries of ELPA
            if '%aocc' in spec:
                libs.append(join_path(elpa.prefix.lib,
                            ('libelpa{elpa_suffix}.a'
                                .format(elpa_suffix=elpa_suffix))))
            else:
                libs.append(join_path(elpa.libs.directories[0],
                            ('libelpa{elpa_suffix}.{dso_suffix}'
                                .format(elpa_suffix=elpa_suffix,
                                        dso_suffix=dso_suffix))))

            if spec.satisfies('@:4'):
                if elpa.satisfies('@:2014.5'):
                    cppflags.append('-D__ELPA')
                elif elpa.satisfies('@2014.6:2015.10'):
                    cppflags.append('-D__ELPA2')
                else:
                    cppflags.append('-D__ELPA3')
            else:
                cppflags.append('-D__ELPA={0}{1:02d}'
                                .format(elpa.version[0],
                                        int(elpa.version[1])))
                fcflags += ['-I{0}'.format(join_path(elpa_incdir, 'elpa'))]

            if '+cuda' in spec and '+cuda' in elpa:
                cppflags += ['-D__ELPA_NVIDIA_GPU']

        if spec.satisfies('+sirius'):
            sirius = spec['sirius']
            cppflags.append('-D__SIRIUS')
            fcflags += ['-I{0}'.format(sirius.prefix.include.sirius)]
            libs += list(sirius.libs)

        if spec.satisfies('+cuda'):
            libs += [
                '-L{}'.format(spec['cuda'].libs.directories[0]),
                '-L{}/stubs'.format(spec['cuda'].libs.directories[0]),
                '-lcuda', '-lcudart', '-lnvrtc', '-lstdc++']

            if spec.satisfies('@9:'):
                acc_compiler_var = 'OFFLOAD_CC'
                acc_flags_var = 'OFFLOAD_FLAGS'
                cppflags += [
                    '-D__DBCSR_ACC',
                    '-D__GRID_CUDA',
                    '-DOFFLOAD_TARGET=cuda',
                ]
                libs += ['-lcublas']
            else:
                acc_compiler_var = 'NVCC'
                acc_flags_var = 'NVFLAGS'
                cppflags += ['-D__ACC']
                if spec.satisfies('+cuda_blas'):
                    cppflags += ['-D__DBCSR_ACC=2']
                    libs += ['-lcublas']
                else:
                    cppflags += ['-D__DBCSR_ACC']

            if spec.satisfies('+cuda_fft'):
                cppflags += ['-D__PW_CUDA']
                libs += ['-lcufft', '-lcublas']

            cuda_arch = spec.variants['cuda_arch'].value[0]
            if cuda_arch:
                gpuver = {
                    '35': 'K40',
                    '37': 'K80',
                    '60': 'P100',
                    '70': 'V100',
                }[cuda_arch]

                if (cuda_arch == '35'
                        and spec.satisfies('+cuda_arch_35_k20x')):
                    gpuver = 'K20X'

        if 'smm=libsmm' in spec:
            lib_dir = join_path(
                'lib', self.makefile_architecture, self.makefile_version
            )
            mkdirp(lib_dir)
            try:
                copy(env['LIBSMM_PATH'], join_path(lib_dir, 'libsmm.a'))
            except KeyError:
                raise KeyError('Point environment variable LIBSMM_PATH to '
                               'the absolute path of the libsmm.a file')
            except IOError:
                raise IOError('The file LIBSMM_PATH pointed to does not '
                              'exist. Note that it must be absolute path.')
            cppflags.extend([
                '-D__HAS_smm_dnn',
                '-D__HAS_smm_vec',
            ])
            libs.append('-lsmm')

        elif 'smm=libxsmm' in spec:
            cppflags += ['-D__LIBXSMM']
            cppflags += pkgconf('--cflags-only-other', 'libxsmmf',
                                output=str).split()
            fcflags += pkgconf('--cflags-only-I', 'libxsmmf',
                               output=str).split()
            libs += pkgconf('--libs', 'libxsmmf', output=str).split()

        if '+libvori' in spec:
            cppflags += ['-D__LIBVORI']
            libvori = spec['libvori'].libs
            ldflags += [libvori.search_flags]
            libs += libvori
            libs += ['-lstdc++']

        if '+spglib' in spec:
            cppflags += ['-D__SPGLIB']
            spglib = spec['spglib'].libs
            ldflags += [spglib.search_flags]
            libs += spglib

        dflags.extend(cppflags)
        cflags.extend(cppflags)
        cxxflags.extend(cppflags)
        fcflags.extend(cppflags)
        nvflags.extend(cppflags)

        with open(self.makefile, 'w') as mkf:
            if '+plumed' in spec:
                mkf.write('# include Plumed.inc as recommended by'
                          'PLUMED to include libraries and flags')
                mkf.write('include {0}\n'.format(
                    spec['plumed'].package.plumed_inc
                ))

            mkf.write('\n# COMPILER, LINKER, TOOLS\n\n')
            mkf.write('FC  = {0}\n'
                      'CC  = {1}\n'
                      'CXX = {2}\n'
                      'LD  = {3}\n'
                      .format(fc, cc, cxx, fc))

            if '%intel' in spec:
                intel_bin_dir = ancestor(self.compiler.cc)
                # CPP is a commented command in Intel arch of CP2K
                # This is the hack through which cp2k developers avoid doing :
                #
                # ${CPP} <file>.F > <file>.f90
                #
                # and use `-fpp` instead
                mkf.write('CPP = # {0} -P\n'.format(spack_cc))
                mkf.write('AR  = {0}/xiar -r\n'.format(intel_bin_dir))
            else:
                mkf.write('CPP = # {0} -E\n'.format(spack_cc))
                mkf.write('AR  = ar -r\n')

            if '+cuda' in spec:
                mkf.write('{0} = {1}\n'.format(
                    acc_compiler_var,
                    join_path(spec['cuda'].prefix, 'bin', 'nvcc')))

            # Write compiler flags to file
            def fflags(var, lst):
                return '{0} = {1}\n\n'.format(
                    var,
                    ' \\\n\t'.join(lst))

            mkf.write('\n# FLAGS & LIBRARIES\n')
            mkf.write(fflags('DFLAGS', dflags))
            mkf.write(fflags('CPPFLAGS', cppflags))
            mkf.write(fflags('CFLAGS', cflags))
            mkf.write(fflags('CXXFLAGS', cxxflags))
            if '+cuda' in spec:
                mkf.write(fflags(acc_flags_var, nvflags))
            mkf.write(fflags('FCFLAGS', fcflags))
            mkf.write(fflags('LDFLAGS', ldflags))
            mkf.write(fflags('LIBS', libs))

            if '%intel' in spec:
                mkf.write(fflags('LDFLAGS_C', ldflags + ['-nofor-main']))

            mkf.write('# CP2K-specific flags\n\n')
            mkf.write('GPUVER = {0}\n'.format(gpuver))
            mkf.write('DATA_DIR = {0}\n'.format(self.prefix.share.data))

    @property
    def build_directory(self):
        build_dir = self.stage.source_path

        if self.spec.satisfies('@:6'):
            # prior to version 7.1 was the Makefile located in makefiles/
            build_dir = join_path(build_dir, 'makefiles')

        return build_dir

    @property
    def build_targets(self):
        return [
            'ARCH={0}'.format(self.makefile_architecture),
            'VERSION={0}'.format(self.makefile_version)
        ]

    def build(self, spec, prefix):
        if '+cuda' in spec and len(spec.variants['cuda_arch'].value) > 1:
            raise InstallError("cp2k supports only one cuda_arch at a time")

        # Apparently the Makefile bases its paths on PWD
        # so we need to set PWD = self.build_directory
        with spack.util.environment.set_env(PWD=self.build_directory):
            super(Cp2k, self).build(spec, prefix)

    def install(self, spec, prefix):
        exe_dir = join_path('exe', self.makefile_architecture)
        install_tree(exe_dir, self.prefix.bin)
        install_tree('data', self.prefix.share.data)

    def check(self):
        data_dir = join_path(self.stage.source_path, 'data')

        # CP2K < 7 still uses $PWD to detect the current working dir
        # and Makefile is in a subdir, account for both facts here:
        with spack.util.environment.set_env(CP2K_DATA_DIR=data_dir,
                                            PWD=self.build_directory):
            with working_dir(self.build_directory):
                make('test', *self.build_targets)
