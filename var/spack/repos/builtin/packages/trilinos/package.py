# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *
from spack.operating_systems.mac_os import macos_version
from spack.pkg.builtin.kokkos import Kokkos

# Trilinos is complicated to build, as an inspiration a couple of links to
# other repositories which build it:
# https://github.com/hpcugent/easybuild-easyblocks/blob/master/easybuild/easyblocks/t/trilinos.py#L111
# https://github.com/koecher/candi/blob/master/deal.II-toolchain/packages/trilinos.package
# https://gitlab.com/configurations/cluster-config/blob/master/trilinos.sh
# https://github.com/Homebrew/homebrew-science/blob/master/trilinos.rb and some
# relevant documentation/examples:
# https://github.com/trilinos/Trilinos/issues/175


class Trilinos(CMakePackage, CudaPackage):
    """The Trilinos Project is an effort to develop algorithms and enabling
    technologies within an object-oriented software framework for the solution
    of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """
    homepage = "https://trilinos.org/"
    url      = "https://github.com/trilinos/Trilinos/archive/trilinos-release-12-12-1.tar.gz"
    git      = "https://github.com/trilinos/Trilinos.git"

    maintainers = ['keitat', 'sethrj', 'kuberry']

    # ###################### Versions ##########################

    version('xsdk-0.2.0', tag='xsdk-0.2.0')
    version('develop', branch='develop')
    version('master', branch='master')
    version('13.0.1', commit='4796b92fb0644ba8c531dd9953e7a4878b05c62d')  # tag trilinos-release-13-0-1
    version('13.0.0', commit='9fec35276d846a667bc668ff4cbdfd8be0dfea08')  # tag trilinos-release-13-0-0
    version('12.18.1', commit='55a75997332636a28afc9db1aee4ae46fe8d93e7')  # tag trilinos-release-12-8-1
    version('12.14.1', sha256='52a4406cca2241f5eea8e166c2950471dd9478ad6741cbb2a7fc8225814616f0')
    version('12.12.1', sha256='5474c5329c6309224a7e1726cf6f0d855025b2042959e4e2be2748bd6bb49e18')
    version('12.10.1', sha256='ab81d917196ffbc21c4927d42df079dd94c83c1a08bda43fef2dd34d0c1a5512')
    version('12.8.1', sha256='d20fe60e31e3ba1ef36edecd88226240a518f50a4d6edcc195b88ee9dda5b4a1')
    version('12.6.4', sha256='1c7104ba60ee8cc4ec0458a1c4f6a26130616bae7580a7b15f2771a955818b73')
    version('12.6.3', sha256='4d28298bb4074eef522db6cd1626f1a934e3d80f292caf669b8846c0a458fe81')
    version('12.6.2', sha256='8be7e3e1166cc05aea7f856cc8033182e8114aeb8f87184cb38873bfb2061779')
    version('12.6.1', sha256='4b38ede471bed0036dcb81a116fba8194f7bf1a9330da4e29c3eb507d2db18db')
    version('12.4.2', sha256='fd2c12e87a7cedc058bcb8357107ffa2474997aa7b17b8e37225a1f7c32e6f0e')
    version('12.2.1', sha256='088f303e0dc00fb4072b895c6ecb4e2a3ad9a2687b9c62153de05832cf242098')
    version('12.0.1', sha256='eee7c19ca108538fa1c77a6651b084e06f59d7c3307dae77144136639ab55980')
    version('11.14.3', sha256='e37fa5f69103576c89300e14d43ba77ad75998a54731008b25890d39892e6e60')
    version('11.14.2', sha256='f22b2b0df7b88e28b992e19044ba72b845292b93cbbb3a948488199647381119')
    version('11.14.1', sha256='f10fc0a496bf49427eb6871c80816d6e26822a39177d850cc62cf1484e4eec07')

    # ###################### Variants ##########################

    # Other
    # not everyone has py-numpy activated, keep it disabled by default to avoid
    # configure errors

    # Build options
    variant('complex', default=False,
            description='Enable complex numbers in Trilinos')
    variant('explicit_template_instantiation',  default=True,
            description='Enable explicit template instantiation (ETI)')
    variant('float', default=False,
            description='Enable single precision (float) numbers in Trilinos')
    variant('gotype', default='long',
            values=('int', 'long', 'long_long', 'all'),
            multi=False,
            description='global ordinal type for Tpetra')
    variant('fortran',      default=True,
            description='Compile with Fortran support')
    variant('python',       default=False,
            description='Build PyTrilinos wrappers')
    variant('wrapper', default=False,
            description="Use nvcc-wrapper for CUDA build")
    variant('cuda_rdc', default=False,
            description='turn on RDC for CUDA build')
    variant('cxxstd', default='11', values=['11', '14', '17'], multi=False)
    variant('openmp',       default=False,
            description='Enable OpenMP')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('debug',       default=False,
            description='Enable runtime safety and debug checks')

    # TPLs (alphabet order)
    variant('boost',        default=False,
            description='Compile with Boost')
    variant('cgns',         default=False,
            description='Enable CGNS')
    variant('adios2',       default=False,
            description='Enable ADIOS2')
    variant('hdf5',         default=False,
            description='Compile with HDF5')
    variant('hypre',        default=False,
            description='Compile with Hypre preconditioner')
    variant('matio',        default=False,
            description='Compile with Matio')
    variant('mpi',          default=True,
            description='Compile with MPI parallelism')
    variant('mumps',        default=False,
            description='Compile with support for MUMPS solvers')
    variant('netcdf',       default=False,
            description='Compile with netcdf')
    variant('pnetcdf',      default=False,
            description='Compile with parallel-netcdf')
    variant('suite-sparse', default=False,
            description='Compile with SuiteSparse solvers')
    variant('superlu-dist', default=False,
            description='Compile with SuperluDist solvers')
    variant('superlu',      default=False,
            description='Compile with SuperLU solvers')
    variant('strumpack',    default=False,
            description='Compile with STRUMPACK solvers')
    variant('zlib',         default=False,
            description='Compile with zlib')

    # Package options (alphabet order)
    variant('amesos',       default=True,
            description='Compile with Amesos')
    variant('amesos2',      default=True,
            description='Compile with Amesos2')
    variant('anasazi',      default=True,
            description='Compile with Anasazi')
    variant('aztec',        default=True,
            description='Compile with Aztec')
    variant('belos',        default=True,
            description='Compile with Belos')
    # chaco is disabled by default. As of 12.14.1 libchaco.so
    # has the global symbol divide (and maybe others) that can
    # lead to symbol clash.
    variant('chaco',       default=False,
            description='Compile with Chaco from SEACAS')
    variant('epetra',       default=True,
            description='Compile with Epetra')
    variant('epetraext',    default=True,
            description='Compile with EpetraExt')
    # Disable Exodus by default as it requires netcdf
    variant('exodus',       default=False,
            description='Compile with Exodus from SEACAS')
    variant('ifpack',       default=True,
            description='Compile with Ifpack')
    variant('ifpack2',      default=True,
            description='Compile with Ifpack2')
    variant('intrepid',     default=False,
            description='Enable Intrepid')
    variant('intrepid2',    default=False,
            description='Enable Intrepid2')
    variant('isorropia',    default=False,
            description='Compile with Isorropia')
    variant('kokkos',       default=True,
            description='Compile with Kokkos')
    variant('ml',           default=True,
            description='Compile with ML')
    variant('minitensor',   default=False,
            description='Compile with MiniTensor')
    variant('muelu',        default=True,
            description='Compile with Muelu')
    variant('nox',          default=False,
            description='Compile with NOX')
    variant('piro',         default=False,
            description='Compile with Piro')
    variant('phalanx',      default=False,
            description='Compile with Phalanx')
    variant('rol',          default=False,
            description='Compile with ROL')
    variant('rythmos',      default=False,
            description='Compile with Rythmos')
    variant('sacado',       default=True,
            description='Compile with Sacado')
    variant('stk',          default=False,
            description='Compile with STK')
    variant('shards',       default=False,
            description='Compile with Shards')
    variant('shylu',        default=False,
            description='Compile with ShyLU')
    variant('stokhos',      default=False,
            description='Compile with Stokhos')
    variant('stratimikos',  default=False,
            description='Compile with Stratimikos')
    variant('teko',         default=False,
            description='Compile with Teko')
    variant('tempus',       default=False,
            description='Compile with Tempus')
    variant('tpetra',       default=True,
            description='Compile with Tpetra')
    variant('trilinoscouplings', default=False,
            description='Compile with TrilinosCouplings')
    variant('zoltan',       default=False,
            description='Compile with Zoltan')
    variant('zoltan2',      default=False,
            description='Compile with Zoltan2')

    # Internal package options (alphabetical order)
    variant('basker',             default=False,
            description='Compile with the Basker solver in Amesos2')
    variant('epetraextbtf',              default=False,
            description='Compile with BTF in EpetraExt')
    variant('epetraextexperimental',     default=False,
            description='Compile with experimental in EpetraExt')
    variant('epetraextgraphreorderings', default=False,
            description='Compile with graph reorderings in EpetraExt')

    # External package options
    variant('dtk',          default=False,
            description='Enable DataTransferKit (deprecated)')
    variant('scorec',       default=False,
            description='Enable SCOREC')
    variant('mesquite',     default=False,
            description='Enable Mesquite (deprecated)')

    resource(name='dtk',
             git='https://github.com/ornl-cees/DataTransferKit.git',
             commit='4fe4d9d56cfd4f8a61f392b81d8efd0e389ee764',  # branch dtk-3.0
             placement='DataTransferKit',
             when='+dtk @12.14.0:12.14.99')
    resource(name='dtk',
             git='https://github.com/ornl-cees/DataTransferKit.git',
             commit='edfa050cd46e2274ab0a0b7558caca0079c2e4ca',  # tag 3.1-rc1
             placement='DataTransferKit',
             submodules=True,
             when='+dtk @12.18:12.18.99')
    resource(name='dtk',
             git='https://github.com/ornl-cees/DataTransferKit.git',
             branch='master',
             placement='DataTransferKit',
             submodules=True,
             when='+dtk @develop')
    resource(name='scorec',
             git='https://github.com/SCOREC/core.git',
             commit='73c16eae073b179e45ec625a5abe4915bc589af2',  # tag v2.2.5
             placement='SCOREC',
             when='+scorec')
    resource(name='mesquite',
             url='https://github.com/trilinos/mesquite/archive/trilinos-release-12-12-1.tar.gz',
             sha256='e0d09b0939dbd461822477449dca611417316e8e8d8268fd795debb068edcbb5',
             placement='packages/mesquite',
             when='+mesquite @12.12.1:12.16.99')
    resource(name='mesquite',
             git='https://github.com/trilinos/mesquite.git',
             commit='20a679679b5cdf15bf573d66c5dc2b016e8b9ca1',  # branch trilinos-release-12-12-1
             placement='packages/mesquite',
             when='+mesquite @12.18.1:12.18.99')
    resource(name='mesquite',
             git='https://github.com/trilinos/mesquite.git',
             tag='develop',
             placement='packages/mesquite',
             when='+mesquite @develop')

    # ###################### Conflicts ##########################

    # Epetra packages
    with when('~epetra'):
        conflicts('+amesos')
        conflicts('+aztec')
        conflicts('+epetraext')
        conflicts('+ifpack')
        conflicts('+isorropia')
    with when('~epetraext'):
        conflicts('+isorropia')
        conflicts('+teko')
        conflicts('+epetraextbtf')
        conflicts('+epetraextexperimental')
        conflicts('+epetraextgraphreorderings')
    conflicts('+teko', when='~amesos')
    conflicts('+teko', when='~anasazi')
    conflicts('+teko', when='~aztec')
    conflicts('+teko', when='~ifpack')
    conflicts('+teko', when='~ml')

    # Tpetra packages
    with when('~kokkos'):
        conflicts('+cuda')
        conflicts('+tpetra')
        conflicts('+intrepid2')
        conflicts('+phalanx')
    with when('~tpetra'):
        conflicts('+amesos2')
        conflicts('+dtk')
        conflicts('+ifpack2')
        conflicts('+teko')
        conflicts('+zoltan2')

    conflicts('+basker', when='~amesos2')
    conflicts('+exodus', when='~netcdf')
    conflicts('+ifpack2', when='~belos')
    conflicts('+intrepid', when='~sacado')
    conflicts('+intrepid', when='~shards')
    conflicts('+intrepid2', when='~shards')
    conflicts('+isorropia', when='~zoltan')
    conflicts('+phalanx', when='~sacado')
    conflicts('+teko', when='~stratimikos')
    conflicts('+teko', when='@:12 gotype=long')
    conflicts('+tempus', when='~nox')
    conflicts('+zoltan2', when='~zoltan')

    # Only allow DTK with Trilinos 12
    conflicts('+dtk', when='~boost')
    conflicts('+dtk', when='~intrepid2')
    conflicts('+dtk', when='@0:12.12.99,develop,master')

    # Only allow Mesquite with older Trilinos 12.12 up to 13
    conflicts('+mesquite', when='@0:12.10.99,master,develop')
    # Can only use one type of SuperLU
    conflicts('+superlu-dist', when='+superlu')
    # For Trilinos v11 we need to force SuperLUDist=OFF, since only the
    # deprecated SuperLUDist v3.3 together with an Amesos patch is working.
    conflicts('+superlu-dist', when='@11.4.1:11.14.3')
    # see https://github.com/trilinos/Trilinos/issues/3566
    conflicts('+superlu-dist', when='+float+amesos2+explicit_template_instantiation^superlu-dist@5.3.0:')
    # Amesos, conflicting types of double and complex SLU_D
    # see
    # https://trilinos.org/pipermail/trilinos-users/2015-March/004731.html
    # and
    # https://trilinos.org/pipermail/trilinos-users/2015-March/004802.html
    conflicts('+superlu-dist', when='+complex+amesos2')
    conflicts('+strumpack', when='@:13.0.99')
    # PnetCDF was only added after v12.10.1
    conflicts('+pnetcdf', when='@0:12.10.1')
    # https://github.com/trilinos/Trilinos/issues/2994
    conflicts(
        '+shared', when='+stk platform=darwin',
        msg='Cannot build Trilinos with STK as a shared library on Darwin.'
    )
    conflicts('+adios2', when='@:12.14.1')
    conflicts('+adios2', when='@xsdk-0.2.0')
    conflicts('+pnetcdf', when='~netcdf')
    conflicts('+pnetcdf', when='~mpi')
    conflicts('+cuda_rdc', when='~cuda')
    conflicts('+wrapper', when='~cuda')
    conflicts('+wrapper', when='%clang')
    conflicts('cxxstd=11', when='@develop')
    conflicts('cxxstd=11', when='+wrapper ^cuda@6.5.14')
    conflicts('cxxstd=14', when='+wrapper ^cuda@6.5.14:8.0.61')
    conflicts('cxxstd=17', when='+wrapper ^cuda@6.5.14:10.2.89')

    # Boost requires minitensor
    conflicts('~boost', when='+minitensor')

    # SCOREC requires shards, stk, and zoltan
    conflicts('+scorec', when='~mpi')
    conflicts('+scorec', when='~shards')
    conflicts('+scorec', when='~stk')
    conflicts('+scorec', when='~zoltan')

    # Multi-value gotype only applies to trilinos through 12.14
    conflicts('gotype=all', when='@12.15:')

    # All compilers except for pgi are in conflict:
    for __compiler in spack.compilers.supported_compilers():
        if __compiler != 'clang':
            conflicts('+cuda', when='~wrapper %{0}'.format(__compiler),
                      msg='trilinos~wrapper+cuda can only be built with the '
                      'Clang compiler')

    # ###################### Dependencies ##########################

    # Explicit dependency variants
    depends_on('adios2', when='+adios2')
    depends_on('blas')
    depends_on('boost', when='+boost')
    depends_on('cgns', when='+cgns')
    depends_on('hdf5+hl', when='+hdf5')
    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('hdf5+mpi', when="+hdf5+mpi")
    depends_on('lapack')
    depends_on('matio', when='+matio')
    depends_on('mpi', when='+mpi')
    depends_on('netcdf-c+mpi+parallel-netcdf', when="+netcdf+pnetcdf@master,12.12.1:")
    depends_on('netcdf-c+mpi', when="+netcdf~pnetcdf+mpi")
    depends_on('netcdf-c', when="+netcdf")
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('zlib', when="+zlib")

    # Trilinos' Tribits config system is limited which makes it very tricky to
    # link Amesos with static MUMPS, see
    # https://trilinos.org/docs/dev/packages/amesos2/doc/html/classAmesos2_1_1MUMPS.html
    # One could work it out by getting linking flags from mpif90 --showme:link
    # (or alike) and adding results to -DTrilinos_EXTRA_LINK_FLAGS together
    # with Blas and Lapack and ScaLAPACK and Blacs and -lgfortran and it may
    # work at the end. But let's avoid all this by simply using shared libs
    depends_on('mumps@5.0:+mpi+shared+openmp', when='+mumps+openmp')
    depends_on('mumps@5.0:+mpi+shared~openmp', when='+mumps~openmp')
    depends_on('scalapack', when='+mumps')
    depends_on('superlu-dist', when='+superlu-dist')
    depends_on('superlu-dist@:4.3', when='@11.14.1:12.6.1+superlu-dist')
    depends_on('superlu-dist@4.4:5.3', when='@12.6.2:12.12.1+superlu-dist')
    depends_on('superlu-dist@5.4:6.2.0', when='@12.12.2:13.0.0+superlu-dist')
    depends_on('superlu-dist@6.3.0:', when='@13.0.1:+superlu-dist')
    depends_on('superlu-dist@develop', when='@develop+superlu-dist')
    depends_on('superlu-dist@xsdk-0.2.0', when='@xsdk-0.2.0+superlu-dist')
    depends_on('superlu+pic@4.3', when='+superlu')
    depends_on('strumpack+shared', when='+strumpack')
    depends_on('scalapack', when='+strumpack+mpi')
    # Trilinos can not be built against 64bit int hypre
    depends_on('hypre~internal-superlu~int64', when='+hypre')
    depends_on('hypre@xsdk-0.2.0~internal-superlu', when='@xsdk-0.2.0+hypre')
    depends_on('hypre@develop~internal-superlu', when='@develop+hypre')
    depends_on('python', when='+python')
    depends_on('py-mpi4py', when='+mpi +python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('swig', when='+python')
    depends_on('kokkos-nvcc-wrapper', when='+wrapper')
    depends_on('hwloc', when='@13: +kokkos')
    depends_on('hwloc+cuda', when='@13: +kokkos+cuda')

    # Variant requirements from packages
    depends_on('metis', when='+zoltan')
    depends_on('libx11', when='+exodus')
    depends_on('parmetis', when='+mpi +zoltan')
    depends_on('parmetis', when='+scorec')

    # ###################### Patches ##########################

    patch('umfpack_from_suitesparse.patch', when='@11.14.1:12.8.1')
    patch('xlf_seacas.patch', when='@12.10.1:12.12.1 %xl')
    patch('xlf_seacas.patch', when='@12.10.1:12.12.1 %xl_r')
    patch('xlf_seacas.patch', when='@12.10.1:12.12.1 %clang')
    patch('xlf_tpetra.patch', when='@12.12.1%xl')
    patch('xlf_tpetra.patch', when='@12.12.1%xl_r')
    patch('xlf_tpetra.patch', when='@12.12.1%clang')
    patch('fix_clang_errors_12_18_1.patch', when='@12.18.1%clang')
    patch('cray_secas_12_12_1.patch', when='@12.12.1%cce')
    patch('cray_secas.patch', when='@12.14.1:%cce')

    # workaround an NVCC bug with c++14 (https://github.com/trilinos/Trilinos/issues/6954)
    # avoid calling deprecated functions with CUDA-11
    patch('fix_cxx14_cuda11.patch', when='@13.0.0:13.0.1 cxxstd=14 ^cuda@11:')
    # Allow building with +teko gotype=long
    patch('https://github.com/trilinos/Trilinos/commit/b17f20a0b91e0b9fc5b1b0af3c8a34e2a4874f3f.patch',
          sha256='dee6c55fe38eb7f6367e1896d6bc7483f6f9ab8fa252503050cc0c68c6340610',
          when='@13.0.0:13.0.1 +teko gotype=long')

    def flag_handler(self, name, flags):
        if self.spec.satisfies('%cce'):
            if name == 'ldflags':
                flags.append('-fuse-ld=gold')
        return (None, None, flags)

    def url_for_version(self, version):
        url = "https://github.com/trilinos/Trilinos/archive/trilinos-release-{0}.tar.gz"
        return url.format(version.dashed)

    def setup_dependent_run_environment(self, env, dependent_spec):
        if '+cuda' in self.spec:
            # currently Trilinos doesn't perform the memory fence so
            # it relies on blocking CUDA kernel launch. This is needed
            # in case the dependent app also run a CUDA backend via Trilinos
            env.set('CUDA_LAUNCH_BLOCKING', '1')

    def setup_dependent_package(self, module, dependent_spec):
        if '+wrapper' in self.spec:
            self.spec.kokkos_cxx = self.spec["kokkos-nvcc-wrapper"].kokkos_cxx
        else:
            self.spec.kokkos_cxx = spack_cxx

    def setup_build_environment(self, env):
        spec = self.spec
        if '+cuda' in spec and '+wrapper' in spec:
            if '+mpi' in spec:
                env.set('OMPI_CXX', spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            else:
                env.set('CXX', spec["kokkos-nvcc-wrapper"].kokkos_cxx)

    def cmake_args(self):
        spec = self.spec
        define = CMakePackage.define
        define_from_variant = self.define_from_variant

        def define_trilinos_enable(cmake_var, spec_var=None):
            if spec_var is None:
                spec_var = cmake_var.lower()
            return define_from_variant('Trilinos_ENABLE_' + cmake_var, spec_var)

        def define_tpl_enable(cmake_var, spec_var=None):
            if spec_var is None:
                spec_var = cmake_var.lower()
            return define_from_variant('TPL_ENABLE_' + cmake_var, spec_var)

        cxx_flags = []
        options = []

        # #################### Base Settings #######################

        options.extend([
            define('Trilinos_VERBOSE_CONFIGURE', False),
            define('Trilinos_ENABLE_TESTS', False),
            define('Trilinos_ENABLE_EXAMPLES', False),
            define('Trilinos_ENABLE_CXX11', True),
            define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            define_trilinos_enable('DEBUG', 'debug'),
            # The following can cause problems on systems that don't have
            # static libraries available for things like dl and pthreads
            # for example when trying to build static libs
            # define_from_variant('TPL_FIND_SHARED_LIBS', 'shared')
            # define('Trilinos_LINK_SEARCH_START_STATIC', '+shared' not in spec)
        ])

        # MPI settings
        options.append(define_tpl_enable('MPI'))
        if '+mpi' in spec:
            # Force Trilinos to use the MPI wrappers instead of raw compilers
            # this is needed on Apple systems that require full resolution of
            # all symbols when linking shared libraries
            options.extend([
                define('CMAKE_C_COMPILER', spec['mpi'].mpicc),
                define('CMAKE_CXX_COMPILER', spec['mpi'].mpicxx),
                define('CMAKE_Fortran_COMPILER', spec['mpi'].mpifc),
                define('MPI_BASE_DIR', spec['mpi'].prefix),
            ])

        # ################## Trilinos Packages #####################

        options.extend([
            define_trilinos_enable('Amesos'),
            define_trilinos_enable('Amesos2'),
            define_trilinos_enable('Anasazi'),
            define_trilinos_enable('AztecOO', 'aztec'),
            define_trilinos_enable('Belos'),
            define_trilinos_enable('Epetra'),
            define_trilinos_enable('EpetraExt'),
            define_trilinos_enable('Ifpack'),
            define_trilinos_enable('Ifpack2'),
            define_trilinos_enable('Intrepid'),
            define_trilinos_enable('Intrepid2'),
            define_trilinos_enable('Isorropia'),
            define_trilinos_enable('Kokkos'),
            define_trilinos_enable('MiniTensor'),
            define_trilinos_enable('Mesquite'),
            define_trilinos_enable('ML'),
            define_trilinos_enable('MueLu'),
            define_trilinos_enable('NOX'),
            define_trilinos_enable('Piro'),
            define_trilinos_enable('Phalanx'),
            define_trilinos_enable('PyTrilinos', 'python'),
            define_trilinos_enable('ROL'),
            define_trilinos_enable('Rythmos'),
            define_trilinos_enable('Sacado'),
            define_trilinos_enable('SCOREC'),
            define_trilinos_enable('Shards'),
            define_trilinos_enable('ShyLU'),
            define_trilinos_enable('STK'),
            define_trilinos_enable('Stokhos'),
            define_trilinos_enable('Stratimikos'),
            define_trilinos_enable('Teko'),
            define_trilinos_enable('Tempus'),
            define_trilinos_enable('Tpetra'),
            define_trilinos_enable('TrilinosCouplings'),
            define_trilinos_enable('Zoltan'),
            define_trilinos_enable('Zoltan2'),
            define_from_variant('EpetraExt_BUILD_BTF', 'epetraextbtf'),
            define_from_variant('EpetraExt_BUILD_EXPERIMENTAL',
                                'epetraextexperimental'),
            define_from_variant('EpetraExt_BUILD_GRAPH_REORDERINGS',
                                'epetraextgraphreorderings'),
            define_from_variant('Amesos2_ENABLE_Basker', 'basker'),
        ])

        if '+dtk' in spec:
            options.extend([
                define('Trilinos_EXTRA_REPOSITORIES', 'DataTransferKit'),
                define('Trilinos_ENABLE_DataTransferKit', True),
            ])

        if '+exodus' in spec:
            options.extend([
                define('Trilinos_ENABLE_SEACAS', True),
                define('Trilinos_ENABLE_SEACASExodus', True),
                define('Trilinos_ENABLE_SEACASIoss', True),
                define('Trilinos_ENABLE_SEACASEpu', True),
                define('Trilinos_ENABLE_SEACASExodiff', True),
                define('Trilinos_ENABLE_SEACASNemspread', True),
                define('Trilinos_ENABLE_SEACASNemslice', True),
            ])
        else:
            options.extend([
                define('Trilinos_ENABLE_SEACASExodus', False),
                define('Trilinos_ENABLE_SEACASIoss', False),
            ])

        if '+chaco' in spec:
            options.extend([
                define('Trilinos_ENABLE_SEACAS', True),
                define('Trilinos_ENABLE_SEACASChaco', True),
            ])
        else:
            # don't disable SEACAS, could be needed elsewhere
            options.extend([
                define('Trilinos_ENABLE_SEACASChaco', False),
                define('Trilinos_ENABLE_SEACASNemslice', False)
            ])

        if '+stratimikos' in spec:
            # Explicitly enable Thyra (ThyraCore is required). If you don't do
            # this, then you get "NOT setting ${pkg}_ENABLE_Thyra=ON since
            # Thyra is NOT enabled at this point!" leading to eventual build
            # errors if using MueLu because `Xpetra_ENABLE_Thyra` is set to
            # off.
            options.append(define('Trilinos_ENABLE_Thyra', True))

            # Add thyra adapters based on package enables
            options.extend(
                define_trilinos_enable('Thyra' + pkg + 'Adapters', pkg.lower())
                for pkg in ['Epetra', 'EpetraExt', 'Tpetra'])

        # ######################### TPLs #############################

        # Enable TPLs based on whether they're in our spec, not whether they're
        # variant names: packages/features should disable availability
        tpl_dep_map = [
            ('ADIOS2', 'adios2'),
            ('BLAS', 'blas'),
            ('Boost', 'boost'),
            ('CGNS', 'cgns'),
            ('HDF5', 'hdf5'),
            ('HYPRE', 'hypre'),
            ('LAPACK', 'lapack'),
            ('Matio', 'matio'),
            ('METIS', 'metis'),
            ('Netcdf', 'netcdf-c'),
            ('STRUMPACK', 'strumpack'),
            ('SuperLU', 'superlu'),
            ('X11', 'libx11'),
            ('Zlib', 'zlib'),
        ]
        if spec.satisfies('@13:'):
            tpl_dep_map.append(('HWLOC', 'hwloc'))
        for tpl_name, dep_name in tpl_dep_map:
            have_dep = (dep_name in spec)
            options.append(define('TPL_ENABLE_' + tpl_name, have_dep))
            if not have_dep:
                continue
            depspec = spec[dep_name]
            options.extend([
                define('TPL_' + tpl_name + '_INCLUDE_DIRS', depspec.prefix.include),
                define(tpl_name + '_ROOT', depspec.prefix),
                define(tpl_name + '_LIBRARY_NAMES', depspec.libs.names),
                define(tpl_name + '_LIBRARY_DIRS', depspec.libs.directories),
            ])

        if '+suite-sparse' in spec:
            options.extend([
                # FIXME: Trilinos seems to be looking for static libs only,
                # patch CMake TPL file?
                define('TPL_ENABLE_Cholmod', False),
                # define('TPL_ENABLE_Cholmod', True),
                # define('Cholmod_LIBRARY_DIRS', (
                #    spec['suite-sparse'].prefix.lib)
                # define('Cholmod_INCLUDE_DIRS', (
                #    spec['suite-sparse'].prefix.include)
                define('TPL_ENABLE_UMFPACK', True),
                define('UMFPACK_LIBRARY_DIRS',
                       spec['suite-sparse'].prefix.lib),
                define('UMFPACK_INCLUDE_DIRS',
                       spec['suite-sparse'].prefix.include),
                define('UMFPACK_LIBRARY_NAMES', [
                    'umfpack', 'amd', 'colamd', 'cholmod', 'suitesparseconfig'
                ]),
            ])
        else:
            options.extend([
                define('TPL_ENABLE_Cholmod', False),
                define('TPL_ENABLE_UMFPACK', False),
            ])

        # METIS and ParMETIS mostly depend on transitive dependencies
        # STRUMPACK and SuperLU-dist, so don't provide a separate variant for
        # them.
        have_metis = 'metis' in spec
        options.append(define('TPL_ENABLE_METIS', have_metis))
        if have_metis:
            options.extend([
                define('METIS_LIBRARY_DIRS', spec['metis'].prefix.lib),
                define('METIS_LIBRARY_NAMES', 'metis'),
                define('TPL_METIS_INCLUDE_DIRS', spec['metis'].prefix.include),
            ])

        have_parmetis = 'parmetis' in spec
        options.append(define('TPL_ENABLE_ParMETIS', have_parmetis))
        if have_parmetis:
            options.extend([
                define('ParMETIS_LIBRARY_DIRS', [
                    spec['parmetis'].prefix.lib, spec['metis'].prefix.lib
                ]),
                define('ParMETIS_LIBRARY_NAMES', ['parmetis', 'metis']),
                define('TPL_ParMETIS_INCLUDE_DIRS', [
                    spec['parmetis'].prefix.include,
                    spec['metis'].prefix.include
                ]),
            ])

        options.append(define_tpl_enable('MUMPS'))
        options.append(define_tpl_enable('SCALAPACK', 'mumps'))
        if '+mumps' in spec:
            scalapack = spec['scalapack'].libs
            options.extend([
                define('MUMPS_LIBRARY_DIRS', spec['mumps'].prefix.lib),
                # order is important!
                define('MUMPS_LIBRARY_NAMES', [
                    'dmumps', 'mumps_common', 'pord'
                ]),
                define('SCALAPACK_LIBRARY_NAMES', scalapack.names),
                define('SCALAPACK_LIBRARY_DIRS', scalapack.directories),
            ])
            # see
            # https://github.com/trilinos/Trilinos/blob/master/packages/amesos/README-MUMPS
            cxx_flags.extend([
                '-DMUMPS_5_0'
            ])

        options.append(define_tpl_enable('SuperLUDist', 'superlu-dist'))
        if '+superlu-dist' in spec:
            options.extend([
                define('KokkosTSQR_ENABLE_Complex', False),
                define('TPL_ENABLE_SuperLUDist', True),
                define('SuperLUDist_LIBRARY_DIRS',
                       spec['superlu-dist'].prefix.lib),
                define('SuperLUDist_INCLUDE_DIRS',
                       spec['superlu-dist'].prefix.include),
            ])
            if spec.satisfies('^superlu-dist@4.0:'):
                options.extend([
                    define('HAVE_SUPERLUDIST_LUSTRUCTINIT_2ARG', True),
                ])

        if '+strumpack' in spec:
            options.append(define('Amesos2_ENABLE_STRUMPACK', True))

        options.append(define_tpl_enable('Pnetcdf'))
        if '+pnetcdf' in spec:
            options.extend([
                define('TPL_Netcdf_Enables_Netcdf4', True),
                define('TPL_Netcdf_PARALLEL', True),
                define('PNetCDF_ROOT', spec['parallel-netcdf'].prefix),
            ])

        if '@13: +kokkos' in spec:
            kkmarch = Kokkos.spack_micro_arch_map.get(spec.target.name, None)
            if kkmarch:
                options.append(define("Kokkos_ARCH_" + kkmarch.upper(), True))

        # ################# Miscellaneous Stuff ######################
        # CUDA
        options.append(define_tpl_enable('CUDA'))
        if '+cuda' in spec:
            options.extend([
                define('Kokkos_ENABLE_CUDA', True),
                define('Kokkos_ENABLE_CUDA_UVM', True),
                define('Kokkos_ENABLE_CUDA_LAMBDA', True)])
            if '+cuda_rdc' in spec:
                options.append(define(
                    'Kokkos_ENABLE_CUDA_RELOCATABLE_DEVICE_CODE',
                    True))
            for iArchCC in spec.variants['cuda_arch'].value:
                options.append(define(
                    "Kokkos_ARCH_" +
                    Kokkos.spack_cuda_arch_map[iArchCC].upper(),
                    True))
            if '+wrapper' in spec:
                cxx_flags.extend(['--expt-extended-lambda'])

        # OpenMP
        options.append(define_trilinos_enable('OpenMP'))
        if '+openmp' in spec:
            options.append(define('Kokkos_ENABLE_OpenMP', True))
            if '+tpetra' in spec:
                options.append(define('Tpetra_INST_OPENMP', True))

        # Fortran lib (assumes clang is built with gfortran!)
        if '+fortran' in spec and (
                spec.satisfies('%gcc') or spec.satisfies('%clang') or
                spec.satisfies('%apple-clang')
        ):
            options.append(define('Trilinos_ENABLE_Fortran', True))
            if '+mpi' in spec:
                libgfortran = os.path.dirname(os.popen(
                    '%s --print-file-name libgfortran.a' %
                    spec['mpi'].mpifc).read())
                options.append(define(
                    'Trilinos_EXTRA_LINK_FLAGS',
                    '-L%s/ -lgfortran' % (libgfortran),
                ))

        # Explicit Template Instantiation (ETI) in Tpetra
        # NOTE: Trilinos will soon move to fixed std::uint64_t for GO and
        # std::int32_t or std::int64_t for local.
        options.append(define_from_variant(
            'Trilinos_ENABLE_EXPLICIT_INSTANTIATION',
            'explicit_template_instantiation'))

        complex_s = spec.variants['complex'].value
        float_s = spec.variants['float'].value
        options.extend([
            define('Teuchos_ENABLE_COMPLEX', complex_s),
            define('Teuchos_ENABLE_FLOAT', float_s),
        ])

        if '+explicit_template_instantiation' in spec and '+tpetra' in spec:
            options.extend([
                define('Tpetra_INST_DOUBLE', True),
                define('Tpetra_INST_COMPLEX_DOUBLE', complex_s),
                define('Tpetra_INST_COMPLEX_FLOAT', float_s and complex_s),
                define('Tpetra_INST_FLOAT', float_s),
                define('Tpetra_INST_SERIAL', True),
            ])

            gotype = spec.variants['gotype'].value
            if gotype == 'all':
                # default in older Trilinos versions to enable multiple GOs
                options.extend([
                    define('Tpetra_INST_INT_INT', True),
                    define('Tpetra_INST_INT_LONG', True),
                    define('Tpetra_INST_INT_LONG_LONG', True),
                ])
            else:
                options.extend([
                    define('Tpetra_INST_INT_INT', gotype == 'int'),
                    define('Tpetra_INST_INT_LONG', gotype == 'long'),
                    define('Tpetra_INST_INT_LONG_LONG', gotype == 'long_long'),
                ])

        # disable due to compiler / config errors:
        if spec.satisfies('%xl') or spec.satisfies('%xl_r'):
            options.extend([
                define('Trilinos_ENABLE_Pamgen', False),
                define('Trilinos_ENABLE_Stokhos', False),
            ])

        if sys.platform == 'darwin':
            options.append(define('Trilinos_ENABLE_FEI', False))
            if '+stk' in spec:
                cxx_flags.extend(['-DSTK_NO_BOOST_STACKTRACE'])

        if sys.platform == 'darwin' and macos_version() >= Version('10.12'):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append(define('CMAKE_MACOSX_RPATH', True))
        else:
            options.append(define('CMAKE_INSTALL_NAME_DIR', self.prefix.lib))

        if spec.satisfies('%intel') and spec.satisfies('@12.6.2'):
            # Panzer uses some std:chrono that is not recognized by Intel
            # Don't know which (maybe all) Trilinos versions this applies to
            # Don't know which (maybe all) Intel versions this applies to
            options.append(define('Trilinos_ENABLE_Panzer', False))

        # collect CXX flags:
        options.append(define('CMAKE_CXX_FLAGS', (' '.join(cxx_flags))))

        # disable due to compiler / config errors:
        options.append(define('Trilinos_ENABLE_Pike', False))

        return options

    @run_after('install')
    def filter_python(self):
        # When trilinos is built with Python, libpytrilinos is included
        # through cmake configure files. Namely, Trilinos_LIBRARIES in
        # TrilinosConfig.cmake contains pytrilinos. This leads to a
        # run-time error: Symbol not found: _PyBool_Type and prevents
        # Trilinos to be used in any C++ code, which links executable
        # against the libraries listed in Trilinos_LIBRARIES.  See
        # https://github.com/Homebrew/homebrew-science/issues/2148#issuecomment-103614509
        # A workaround is to remove PyTrilinos from the COMPONENTS_LIST :
        if '+python' in self.spec:
            filter_file(r'(SET\(COMPONENTS_LIST.*)(PyTrilinos;)(.*)',
                        (r'\1\3'),
                        '%s/cmake/Trilinos/TrilinosConfig.cmake' %
                        self.prefix.lib)

    def setup_run_environment(self, env):
        if '+exodus' in self.spec:
            env.prepend_path('PYTHONPATH',
                             self.prefix.lib)

        if '+cuda' in self.spec:
            # currently Trilinos doesn't perform the memory fence so
            # it relies on blocking CUDA kernel launch.
            env.set('CUDA_LAUNCH_BLOCKING', '1')
