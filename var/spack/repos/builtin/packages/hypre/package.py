##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import sys


class Hypre(Package, CudaPackage):
    """Hypre is a library of high performance preconditioners that
       features parallel multigrid methods for both structured and
       unstructured grid problems."""

    homepage = "http://computation.llnl.gov/project/linear_solvers/software.php"
    url      = "http://computation.llnl.gov/project/linear_solvers/download/hypre-2.10.0b.tar.gz"

    version('2.14.0', 'c52c45f01d93fccc7b4d64f429e3696579924463',
            url='https://github.com/LLNL/hypre/archive/v2.14.0.tar.gz')
    version('2.13.0', '4b688a5c15b6b5e3de5e045ae081b89b',
            url='https://github.com/LLNL/hypre/archive/v2.13.0.tar.gz')
    version('2.12.1', 'c6fcb6d7e57cec1c7ce4a44da885068c',
            url='https://github.com/LLNL/hypre/archive/v2.12.1.tar.gz')
    version('2.11.2', 'd507943a1a3ce5681c3308e2f3a6dd34')
    version('2.11.1', '3f02ef8fd679239a6723f60b7f796519')
    version('2.10.1', 'dc048c4cabb3cd549af72591474ad674')
    version('2.10.0b', '768be38793a35bb5d055905b271f5b8e')
    version('develop', git='https://github.com/LLNL/hypre', tag='master')
    version('xsdk-0.2.0', git='https://github.com/LLNL/hypre', tag='xsdk-0.2.0')

    # hypre does not know how to build shared libraries on Darwin
    variant('shared', default=(sys.platform != 'darwin'),
            description="Build shared library (disables static library)")
    # SuperluDist have conflicting headers with those in Hypre
    variant('internal-superlu', default=False,
            description="Use internal Superlu routines")
    variant('int64', default=False,
            description="Use 64bit integers")
    variant('mpi', default=True, description='Enable MPI support')
    variant('fei', default=False, description='Use internal FEI routines')
    variant('openmp', default=False, description='Use OpenMP')
    variant('complex', default=False, description='Use complex values')
    variant('superlu', default=False,
            description='Use external SuperLU library')
    variant('superlu-dist', default=False,
            description='Use external SuperLU_DIST library')

    depends_on("mpi", when='+mpi')
    depends_on("blas")
    depends_on("lapack")
    depends_on('cuda@8:', when='+cuda')
    depends_on('superlu', when='@2.13.0:+superlu')
    depends_on('superlu-dist', when='@2.13.0:+superlu-dist')

    # GPU support was added in 2.13.0
    conflicts('+cuda', when='@:2.12.99')
    # The internal SuperLU was removed in 2.13.0
    conflicts('+internal-superlu', when='@2.13.0:')
    # Use of external SuperLU and SuperLU_DIST was added in 2.13.0
    conflicts('+superlu', when='@:2.12.99')
    conflicts('+superlu-dist', when='@:2.12.99')
    # The required minimum cuda_arch is sm_30.
    conflicts('cuda_arch=,', when='+cuda', msg='cuda_arch must be set')
    conflicts('cuda_arch=20', when='+cuda', msg='minimum cuda_arch is 30')

    # Patch to add ppc64le in config.guess
    patch('ibm-ppc64le.patch', when='@:2.11.1')
    # Patch for building v2.13.0 with cuda
    patch('hypre-2.13.0-cuda.patch', when='@2.13.0+cuda')
    # Patch for building v2.14.0 with cuda
    patch('hypre-2.14.0-cuda.patch', when='@2.14.0+cuda')

    def install(self, spec, prefix):
        # Note: --with-(lapack|blas)-libs= needs space separated list of names
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs

        # TODO: C++ is only needed when 'fei' is enabled?
        configure_args = [
            '--prefix=%s' % prefix,
            '--with-lapack-libs=%s' % ' '.join(lapack.names),
            '--with-lapack-lib-dirs=%s' % ' '.join(lapack.directories),
            '--with-blas-libs=%s' % ' '.join(blas.names),
            '--with-blas-lib-dirs=%s' % ' '.join(blas.directories)
        ]
        make_args = []

        if '+mpi' in self.spec:
            configure_args += ['--with-MPI']
            env['CC'] = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx
        else:
            configure_args.append('--without-MPI')

        cflags = spec.compiler_flags['cflags']
        cxxflags = spec.compiler_flags['cxxflags']
        fflags = spec.compiler_flags['fflags']
        ldflags = spec.compiler_flags['ldflags']

        if cflags:
            configure_args += ['CFLAGS=%s' % ' '.join(cflags)]
        if cxxflags:
            configure_args += ['CXXFLAGS=%s' % ' '.join(cxxflags)]
        if fflags:
            configure_args += ['FCFLAGS=%s' % ' '.join(fflags)]

        if '+int64' in self.spec:
            configure_args.append('--enable-bigint')

        if '+shared' in self.spec:
            configure_args.append("--enable-shared")

        if '@:2.12.99~internal-superlu' in self.spec:
            configure_args.append("--without-superlu")
            # MLI and FEI do not build without superlu on Linux
            configure_args.append("--without-mli")
            configure_args.append("--without-fei")

        if '@2.13.0:+superlu' in self.spec:
            superlu = spec['superlu']
            configure_args += [
                "--with-superlu",
                "--with-superlu-include=%s" % superlu.prefix.include,
                "--with-superlu-lib=%s" % superlu.libs.ld_flags]
            if '+shared' in spec:
                ldflags += [superlu.libs.ld_flags]

        if '+superlu-dist' in self.spec:
            superlu_dist = spec['superlu-dist']
            parmetis = spec['parmetis']
            metis = spec['metis']
            superlu_dist_libs = superlu_dist.libs + parmetis.libs + metis.libs
            configure_args += [
                "--with-dsuperlu",
                "--with-dsuperlu-include=%s %s" %
                (superlu_dist.prefix.include, parmetis.prefix.include),
                "--with-dsuperlu-lib=%s" % superlu_dist_libs.ld_flags]
            if '+shared' in spec:
                ldflags += [superlu_dist_libs.ld_flags]

        configure_args.append(
            '--with%s-fei' % ('' if '+fei' in spec else 'out'))

        configure_args.append(
            '--with%s-openmp' % ('' if '+openmp' in spec else 'out'))

        configure_args.append(
            '--%s-complex' % ('enable' if '+complex' in spec else 'disable'))

        if '@2.13.0,2.14.0+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            cuda_arch = tuple(ca for ca in cuda_arch if ca != '')
            cuda_arch_flags = self.cuda_flags(cuda_arch)
            configure_args += ['--with-cuda', '--enable-unified-memory']
            if spec.version == Version('2.13.0'):
                configure_args += ['--with-nvcc']
            # The nvcc compiler will be used for compiling all files
            nvcc = str(spec['cuda'].prefix.bin.nvcc)
            # Flags used for compiling mixed CUDA and C/C++ files with file
            # extensions different from .cu
            cflags_orig = list(cflags)
            cflags = ['-O2', '--x cu', '-ccbin=%s' % env['CXX'],
                      '--std=c++11', '-expt-extended-lambda',
                      '-DUSE_NVTX', '-DHYPRE_USE_GPU', '-DHYPRE_USE_MANAGED',
                      '-DHYPRE_USE_CUDA', '-DHYPRE_MEMORY_GPU',
                      '-DHAVE_CONFIG_H', '--relocatable-device-code=true']
            if 'essl' in spec:
                cflags += ['-D_ESVCPTR']
            # Flags used for compiling .cu files
            cuflags = ['-O2', '-ccbin=%s' % env['CXX'],
                       '-I.', '-I..', '-I../utilities',
                       '-I%s' % spec['mpi'].prefix.include,
                       '-DUSE_NVTX', '-DHYPRE_USE_GPU',
                       '-DHYPRE_USE_MANAGED', '-DHYPRE_MEMORY_GPU']
            # Flags common for cflags and cuflags
            common_flags = list(cuda_arch_flags)
            if '+shared' in spec:
                common_flags += ['-Xcompiler', self.compiler.pic_flag]
            if '+openmp' in spec:
                common_flags += ['-Xcompiler', self.compiler.openmp_flag]
            cflags += common_flags
            cuflags += common_flags

            cflags_joined = ' '.join(cflags + cflags_orig)
            cxxflags_joined = ' '.join(cflags + cxxflags)
            make_args += [
                'CC=%s' % nvcc,
                'CXX=%s' % nvcc,
                'NVCC=%s' % nvcc,
                'CFLAGS=%s $(C_COMPILE_FLAGS)' % cflags_joined,
                'CXXFLAGS=%s $(CXX_COMPILE_FLAGS)' % cxxflags_joined,
                'NVCCFLAGS=%s' % ' '.join(cuflags)]

            ldflags += [self.hypre_cuda_libs.ld_flags]

            if '+shared' in spec:
                # Additional options for linking a shared library
                # ${BUILD_CC_SHARED} -o ${SONAME} ${FILES_HYPRE} ${SOLIBS}
                #   ${SHARED_SET_SONAME}${SONAME} ${SHARED_OPTIONS} ${LDFLAGS}
                make_args += [
                    'BUILD_CC_SHARED=%s -shared -ccbin=%s' %
                    (' '.join([nvcc] + cuda_arch_flags), env['CXX']),
                    'SHARED_SET_SONAME=-Xlinker -soname,',
                    'SHARED_OPTIONS=',
                    'LIBS=']
                # Patch src/struct_ls/Makefile to link with
                # ../utilities/random.o
                with working_dir(join_path('src', 'struct_ls')):
                    filter_file('^(OBJS\s*=.*)$',
                                '\\1 ../utilities/random.o',
                                'Makefile')
                # ../parcsr_ls/par_relax.o --> src/sstruct_ls/Makefile
                with working_dir(join_path('src', 'sstruct_ls')):
                    filter_file('^(OBJS\s*=.*)$',
                                '\\1 ../parcsr_ls/par_relax.o',
                                'Makefile')

        # Set LDFLAGS - used for linking the shared library and for linking
        # the tests.
        make_args += ['LDFLAGS=%s' % ' '.join(ldflags)]

        # Hypre's source is staged under ./src so we'll have to manually
        # cd into it.
        with working_dir("src"):
            configure(*configure_args)

            make(*make_args)
            if self.run_tests:
                make("check", *make_args)
                make("test", *make_args)
                Executable(join_path('test', 'ij'))()
                sstruct = Executable(join_path('test', 'struct'))
                sstruct()
                sstruct('-in', 'test/sstruct.in.default', '-solver', '40',
                        '-rhsone')
            make("install", *make_args)

    @property
    def hypre_cuda_libs(self):
        cuda_lib_names = ['cusparse', 'cudart', 'cublas', 'nvToolsExt']
        cuda_lib_dirs = [join_path(self.spec['cuda'].prefix, p)
                         for p in ['lib64', 'lib']]
        for dir in cuda_lib_dirs:
            cuda_libs = find_libraries(
                ['lib%s' % n for n in cuda_lib_names], dir,
                shared=True, recursive=False)
            if cuda_libs:
                break
        if not cuda_libs:
            raise RuntimeError('CUDA libraries not found in %s' %
                               cuda_lib_dirs)
        return cuda_libs

    @property
    def headers(self):
        """Export the main hypre header, HYPRE.h; all other headers can be found
        in the same directory.
        Sample usage: spec['hypre'].headers.cpp_flags
        """
        hdrs = find_headers('HYPRE', self.prefix.include, recursive=False)
        return hdrs or None

    @property
    def libs(self):
        """Export the hypre library.
        Sample usage: spec['hypre'].libs.ld_flags
        """
        search_paths = [[self.prefix.lib, False], [self.prefix.lib64, False],
                        [self.prefix, True]]
        is_shared = '+shared' in self.spec
        for path, recursive in search_paths:
            libs = find_libraries('libHYPRE', root=path,
                                  shared=is_shared, recursive=recursive)
            if libs:
                return libs
        return None
