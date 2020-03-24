# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from spack import *
from spack.operating_systems.mac_os import macos_version

# Trilinos is complicated to build, as an inspiration a couple of links to
# other repositories which build it:
# https://github.com/hpcugent/easybuild-easyblocks/blob/master/easybuild/easyblocks/t/trilinos.py#L111
# https://github.com/koecher/candi/blob/master/deal.II-toolchain/packages/trilinos.package
# https://gitlab.com/configurations/cluster-config/blob/master/trilinos.sh
# https://github.com/Homebrew/homebrew-science/blob/master/trilinos.rb and some
# relevant documentation/examples:
# https://github.com/trilinos/Trilinos/issues/175


class Trilinos(CMakePackage):
    """The Trilinos Project is an effort to develop algorithms and enabling
    technologies within an object-oriented software framework for the solution
    of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """
    homepage = "https://trilinos.org/"
    url      = "https://github.com/trilinos/Trilinos/archive/trilinos-release-12-12-1.tar.gz"
    git      = "https://github.com/trilinos/Trilinos.git"

    maintainers = ['aprokop', 'keitat']

    # ###################### Versions ##########################

    version('xsdk-0.2.0', tag='xsdk-0.2.0')
    version('develop', branch='develop')
    version('master', branch='master')
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
    variant('python',       default=False,
            description='Build python wrappers')

    # Build options
    variant('complex', default=False,
            description='Enable complex numbers in Trilinos')
    variant('explicit_template_instantiation',  default=True,
            description='Enable explicit template instantiation (ETI)')
    variant('float', default=False,
            description='Enable single precision (float) numbers in Trilinos')
    variant('gotype', default='long',
            values=('int', 'long', 'long_long'),
            multi=False,
            description='global ordinal type for Tpetra')
    variant('fortran',      default=True,
            description='Compile with Fortran support')
    variant('openmp',       default=False,
            description='Enable OpenMP')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('debug',       default=False,
            description='Enable runtime safety and debug checks')
    variant('xsdkflags',    default=False,
            description='Compile using the default xSDK configuration')

    # TPLs (alphabet order)
    variant('boost',        default=True,
            description='Compile with Boost')
    variant('cgns',         default=False,
            description='Enable CGNS')
    variant('adios2',       default=False,
            description='Enable ADIOS2')
    variant('glm',          default=True,
            description='Compile with GLM')
    variant('gtest',        default=True,
            description='Compile with Gtest')
    variant('hdf5',         default=True,
            description='Compile with HDF5')
    variant('hypre',        default=True,
            description='Compile with Hypre preconditioner')
    variant('matio',        default=True,
            description='Compile with Matio')
    variant('metis',        default=True,
            description='Compile with METIS and ParMETIS')
    variant('mumps',        default=True,
            description='Compile with support for MUMPS solvers')
    variant('netcdf',       default=True,
            description='Compile with netcdf')
    variant('pnetcdf',      default=False,
            description='Compile with parallel-netcdf')
    variant('suite-sparse', default=True,
            description='Compile with SuiteSparse solvers')
    variant('superlu-dist', default=False,
            description='Compile with SuperluDist solvers')
    variant('superlu',      default=False,
            description='Compile with SuperLU solvers')
    variant('x11',          default=False,
            description='Compile with X11')
    variant('zlib',         default=False,
            description='Compile with zlib')

    # Package options (alphabet order)
    variant('alloptpkgs',   default=False,
            description='Compile with all optional packages')
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
    variant('exodus',       default=True,
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
    variant('teko',         default=False,
            description='Compile with Teko')
    variant('tempus',       default=False,
            description='Compile with Tempus')
    variant('teuchos',      default=True,
            description='Compile with Teuchos')
    variant('tpetra',       default=True,
            description='Compile with Tpetra')
    variant('zoltan',       default=True,
            description='Compile with Zoltan')
    variant('zoltan2',      default=True,
            description='Compile with Zoltan2')

    # External package options
    variant('dtk',          default=False,
            description='Enable DataTransferKit')
    variant('fortrilinos',  default=False,
            description='Enable ForTrilinos')
    variant('mesquite',     default=False,
            description='Enable Mesquite')

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
    resource(name='fortrilinos',
             git='https://github.com/trilinos/ForTrilinos.git',
             tag='develop',
             placement='packages/ForTrilinos',
             when='+fortrilinos')
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

    conflicts('+amesos2', when='~teuchos')
    conflicts('+amesos2', when='~tpetra')
    conflicts('+amesos', when='~epetra')
    conflicts('+amesos', when='~teuchos')
    conflicts('+anasazi', when='~teuchos')
    conflicts('+belos', when='~teuchos')
    conflicts('+epetraext', when='~epetra')
    conflicts('+epetraext', when='~teuchos')
    conflicts('+ifpack2', when='~belos')
    conflicts('+ifpack2', when='~teuchos')
    conflicts('+ifpack2', when='~tpetra')
    conflicts('+ifpack', when='~epetra')
    conflicts('+ifpack', when='~teuchos')
    conflicts('+intrepid2', when='~kokkos')
    conflicts('+intrepid2', when='~shards')
    conflicts('+intrepid2', when='~teuchos')
    conflicts('+intrepid', when='~sacado')
    conflicts('+intrepid', when='~shards')
    conflicts('+intrepid', when='~teuchos')
    conflicts('+isorropia', when='~epetra')
    conflicts('+isorropia', when='~epetraext')
    conflicts('+isorropia', when='~teuchos')
    conflicts('+isorropia', when='~zoltan')
    conflicts('+muelu', when='~teuchos')
    conflicts('+muelu', when='~xpetra')
    conflicts('+nox', when='~teuchos')
    conflicts('+phalanx', when='~kokkos')
    conflicts('+phalanx', when='~sacado')
    conflicts('+phalanx', when='~teuchos')
    conflicts('+piro', when='~teuchos')
    conflicts('+rol', when='~teuchos')
    conflicts('+rythmos', when='~teuchos')
    conflicts('+teko', when='~amesos')
    conflicts('+teko', when='~anasazi')
    conflicts('+teko', when='~aztec')
    conflicts('+teko', when='~ifpack')
    conflicts('+teko', when='~ml')
    conflicts('+teko', when='~teuchos')
    conflicts('+teko', when='~tpetra')
    conflicts('+tempus', when='~nox')
    conflicts('+tempus', when='~teuchos')
    conflicts('+tpetra', when='~kokkos')
    conflicts('+tpetra', when='~teuchos')
    conflicts('+zoltan2', when='~teuchos')
    conflicts('+zoltan2', when='~tpetra')
    conflicts('+zoltan2', when='~xpetra')
    conflicts('+zoltan2', when='~zoltan')

    conflicts('+dtk', when='~intrepid2')
    conflicts('+dtk', when='~kokkos')
    conflicts('+dtk', when='~teuchos')
    conflicts('+dtk', when='~tpetra')
    # Only allow DTK with Trilinos 12.14 and develop
    conflicts('+dtk', when='@0:12.12.99,master')
    conflicts('+fortrilinos', when='~fortran')
    conflicts('+fortrilinos', when='@:99')
    conflicts('+fortrilinos', when='@master')
    # Only allow Mesquite with Trilinos 12.12 and up, and develop
    conflicts('+mesquite', when='@0:12.10.99,master')
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
    # PnetCDF was only added after v12.10.1
    conflicts('+pnetcdf', when='@0:12.10.1')
    # https://github.com/trilinos/Trilinos/issues/2994
    conflicts(
        '+shared', when='+stk platform=darwin',
        msg='Cannot build Trilinos with STK as a shared library on Darwin.'
    )
    # ADIOS2 was only added after v12.14.1
    conflicts('+adios2', when='@:12.14.1')
    conflicts('+adios2', when='@xsdk-0.2.0')
    conflicts('+pnetcdf', when='~netcdf')

    # ###################### Dependencies ##########################

    # Everything should be compiled position independent (-fpic)
    depends_on('blas')
    depends_on('lapack')
    depends_on('boost', when='+boost')
    depends_on('boost', when='+dtk')
    depends_on('matio', when='+matio')
    depends_on('glm', when='+glm')
    depends_on('metis@5:', when='+metis')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('zlib', when="+zlib")

    # MPI related dependencies
    depends_on('mpi')
    depends_on('netcdf-c+mpi', when="+netcdf~pnetcdf")
    depends_on('netcdf-c+mpi+parallel-netcdf', when="+netcdf+pnetcdf@master,12.12.1:")
    depends_on('parallel-netcdf', when="+netcdf+pnetcdf@master,12.12.1:")
    depends_on('parmetis', when='+metis')
    depends_on('cgns', when='+cgns')
    depends_on('adios2', when='+adios2')
    # Trilinos' Tribits config system is limited which makes it very tricky to
    # link Amesos with static MUMPS, see
    # https://trilinos.org/docs/dev/packages/amesos2/doc/html/classAmesos2_1_1MUMPS.html
    # One could work it out by getting linking flags from mpif90 --showme:link
    # (or alike) and adding results to -DTrilinos_EXTRA_LINK_FLAGS together
    # with Blas and Lapack and ScaLAPACK and Blacs and -lgfortran and it may
    # work at the end. But let's avoid all this by simply using shared libs
    depends_on('mumps@5.0:+mpi+shared', when='+mumps')
    depends_on('scalapack', when='+mumps')
    depends_on('superlu-dist', when='+superlu-dist')
    depends_on('superlu-dist@:4.3', when='@11.14.1:12.6.1+superlu-dist')
    depends_on('superlu-dist@4.4:5.3', when='@12.6.2:12.12.1+superlu-dist')
    depends_on('superlu-dist@develop', when='@develop+superlu-dist')
    depends_on('superlu-dist@xsdk-0.2.0', when='@xsdk-0.2.0+superlu-dist')
    depends_on('superlu+pic@4.3', when='+superlu')
    # Trilinos can not be built against 64bit int hypre
    depends_on('hypre~internal-superlu~int64', when='+hypre')
    depends_on('hypre@xsdk-0.2.0~internal-superlu', when='@xsdk-0.2.0+hypre')
    depends_on('hypre@develop~internal-superlu', when='@develop+hypre')
    # We need hdf5+hl to match with netcdf during concretization
    depends_on('hdf5+hl+mpi', when='+hdf5')
    depends_on('python', when='+python')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('swig', when='+python')

    patch('umfpack_from_suitesparse.patch', when='@11.14.1:12.8.1')
    patch('xlf_seacas.patch', when='@12.10.1:12.12.1 %xl')
    patch('xlf_seacas.patch', when='@12.10.1:12.12.1 %xl_r')
    patch('xlf_seacas.patch', when='@12.10.1:12.12.1 %clang')
    patch('xlf_tpetra.patch', when='@12.12.1%xl')
    patch('xlf_tpetra.patch', when='@12.12.1%xl_r')
    patch('xlf_tpetra.patch', when='@12.12.1%clang')
    patch('fix_clang_errors_12_18_1.patch', when='@12.18.1%clang')

    def url_for_version(self, version):
        url = "https://github.com/trilinos/Trilinos/archive/trilinos-release-{0}.tar.gz"
        return url.format(version.dashed)

    def cmake_args(self):
        spec = self.spec

        cxx_flags = []
        options = []

        # #################### Base Settings #######################

        mpi_bin = spec['mpi'].prefix.bin
        options.extend([
            '-DTrilinos_VERBOSE_CONFIGURE:BOOL=OFF',
            '-DTrilinos_ENABLE_TESTS:BOOL=OFF',
            '-DTrilinos_ENABLE_EXAMPLES:BOOL=OFF',
            '-DTrilinos_ENABLE_CXX11:BOOL=ON',
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DTrilinos_ENABLE_DEBUG:BOOL=%s' % (
                'ON' if '+debug' in spec else 'OFF'),

            # The following can cause problems on systems that don't have
            # static libraries available for things like dl and pthreads
            # for example when trying to build static libs
            # '-DTPL_FIND_SHARED_LIBS:BOOL=%s' % (
            #     'ON' if '+shared' in spec else 'OFF'),
            # '-DTrilinos_LINK_SEARCH_START_STATIC:BOOL=%s' % (
            #     'OFF' if '+shared' in spec else 'ON'),

            # Force Trilinos to use the MPI wrappers instead of raw compilers
            # this is needed on Apple systems that require full resolution of
            # all symbols when linking shared libraries
            '-DTPL_ENABLE_MPI:BOOL=ON',
            '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DMPI_BASE_DIR:PATH=%s'      % spec['mpi'].prefix
        ])

        # ################## Trilinos Packages #####################

        options.extend([
            '-DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=%s' % (
                'ON' if '+alloptpkgs' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Amesos:BOOL=%s' % (
                'ON' if '+amesos' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Amesos2:BOOL=%s' % (
                'ON' if '+amesos2' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Anasazi:BOOL=%s' % (
                'ON' if '+anasazi' in spec else 'OFF'),
            '-DTrilinos_ENABLE_AztecOO:BOOL=%s' % (
                'ON' if '+aztec' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Belos:BOOL=%s' % (
                'ON' if '+belos' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Epetra:BOOL=%s' % (
                'ON' if '+epetra' in spec else 'OFF'),
            '-DTrilinos_ENABLE_EpetraExt:BOOL=%s' % (
                'ON' if '+epetraext' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Ifpack:BOOL=%s' % (
                'ON' if '+ifpack' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Ifpack2:BOOL=%s' % (
                'ON' if '+ifpack2' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Intrepid=%s' % (
                'ON' if '+intrepid' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Intrepid2=%s' % (
                'ON' if '+intrepid2' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Isorropia=%s' % (
                'ON' if '+isorropia' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Kokkos:BOOL=%s' % (
                'ON' if '+kokkos' in spec else 'OFF'),
            '-DTrilinos_ENABLE_MiniTensor=%s' % (
                'ON' if '+minitensor' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Mesquite:BOOL=%s' % (
                'ON' if '+mesquite' in spec else 'OFF'),
            '-DTrilinos_ENABLE_ML:BOOL=%s' % (
                'ON' if '+ml' in spec else 'OFF'),
            '-DTrilinos_ENABLE_MueLu:BOOL=%s' % (
                'ON' if '+muelu' in spec else 'OFF'),
            '-DTrilinos_ENABLE_NOX:BOOL=%s' % (
                'ON' if '+nox' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Piro:BOOL=%s' % (
                'ON' if '+piro' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Phalanx=%s' % (
                'ON' if '+phalanx' in spec else 'OFF'),
            '-DTrilinos_ENABLE_PyTrilinos:BOOL=%s' % (
                'ON' if '+python' in spec else 'OFF'),
            '-DTrilinos_ENABLE_ROL:BOOL=%s' % (
                'ON' if '+rol' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Rythmos=%s' % (
                'ON' if '+rythmos' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Sacado:BOOL=%s' % (
                'ON' if '+sacado' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Shards=%s' % (
                'ON' if '+shards' in spec else 'OFF'),
            '-DTrilinos_ENABLE_ShyLU=%s' % (
                'ON' if '+shylu' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Teko=%s' % (
                'ON' if '+teko' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Tempus=%s' % (
                'ON' if '+tempus' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Teuchos:BOOL=%s' % (
                'ON' if '+teuchos' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Tpetra:BOOL=%s' % (
                'ON' if '+tpetra' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Zoltan:BOOL=%s' % (
                'ON' if '+zoltan' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Zoltan2:BOOL=%s' % (
                'ON' if '+zoltan2' in spec else 'OFF'),
        ])

        if '+xsdkflags' in spec:
            options.extend(['-DUSE_XSDK_DEFAULTS=YES'])

        if '+stk' in spec:
            options.extend([
                '-DTrilinos_ENABLE_STK:BOOL=ON'
            ])
        else:
            options.extend([
                '-DTrilinos_ENABLE_STK:BOOL=OFF'
            ])

        if '+dtk' in spec:
            options.extend([
                '-DTrilinos_EXTRA_REPOSITORIES:STRING=DataTransferKit',
                '-DTrilinos_ENABLE_DataTransferKit:BOOL=ON'
            ])

        if '+exodus' in spec:
            options.extend([
                '-DTrilinos_ENABLE_SEACAS:BOOL=ON',
                '-DTrilinos_ENABLE_SEACASExodus:BOOL=ON',
                '-DTrilinos_ENABLE_SEACASIoss:BOOL=ON',
                '-DTrilinos_ENABLE_SEACASEpu:BOOL=ON',
                '-DTrilinos_ENABLE_SEACASExodiff:BOOL=ON',
                '-DTrilinos_ENABLE_SEACASNemspread:BOOL=ON',
                '-DTrilinos_ENABLE_SEACASNemslice:BOOL=ON'
            ])
        else:
            options.extend([
                '-DTrilinos_ENABLE_SEACASExodus:BOOL=OFF',
                '-DTrilinos_ENABLE_SEACASIoss:BOOL=OFF'
            ])

        if '+chaco' in spec:
            options.extend([
                '-DTrilinos_ENABLE_SEACAS:BOOL=ON'
                '-DTrilinos_ENABLE_SEACASChaco:BOOL=ON'
            ])
        else:
            # don't disable SEACAS, could be needed elsewhere
            options.extend([
                '-DTrilinos_ENABLE_SEACASChaco:BOOL=OFF',
                '-DTrilinos_ENABLE_SEACASNemslice=OFF'
            ])

        # ######################### TPLs #############################

        blas = spec['blas'].libs
        lapack = spec['lapack'].libs
        # Note: -DXYZ_LIBRARY_NAMES= needs semicolon separated list of names
        options.extend([
            '-DTPL_ENABLE_BLAS=ON',
            '-DBLAS_LIBRARY_NAMES=%s' % ';'.join(blas.names),
            '-DBLAS_LIBRARY_DIRS=%s' % ';'.join(blas.directories),
            '-DTPL_ENABLE_LAPACK=ON',
            '-DLAPACK_LIBRARY_NAMES=%s' % ';'.join(lapack.names),
            '-DLAPACK_LIBRARY_DIRS=%s' % ';'.join(lapack.directories),
            '-DTPL_ENABLE_GLM:BOOL=%s' % ('ON' if '+glm' in spec else 'OFF'),
            '-DTPL_ENABLE_Matio:BOOL=%s' % (
                'ON' if '+matio' in spec else 'OFF'),
            '-DTPL_ENABLE_X11:BOOL=%s' % (
                'ON' if '+x11' in spec else 'OFF'),
            '-DTrilinos_ENABLE_Gtest:BOOL=%s' % (
                'ON' if '+gtest' in spec else 'OFF'),
        ])

        if '+netcdf' in spec:
            options.extend([
                '-DTPL_ENABLE_Netcdf:BOOL=ON',
                '-DNetCDF_ROOT:PATH=%s' % spec['netcdf-c'].prefix
            ])
        else:
            options.extend(['-DTPL_ENABLE_Netcdf:BOOL=OFF'])

        if '+hypre' in spec:
            options.extend([
                '-DTPL_ENABLE_HYPRE:BOOL=ON',
                '-DHYPRE_INCLUDE_DIRS:PATH=%s' % spec['hypre'].prefix.include,
                '-DHYPRE_LIBRARY_DIRS:PATH=%s' % spec['hypre'].prefix.lib
            ])

        if '+boost' in spec:
            options.extend([
                '-DTPL_ENABLE_Boost:BOOL=ON',
                '-DBoost_INCLUDE_DIRS:PATH=%s' % spec['boost'].prefix.include,
                '-DBoost_LIBRARY_DIRS:PATH=%s' % spec['boost'].prefix.lib
            ])
        else:
            options.extend(['-DTPL_ENABLE_Boost:BOOL=OFF'])

        if '+hdf5' in spec:
            options.extend([
                '-DTPL_ENABLE_HDF5:BOOL=ON',
                '-DHDF5_INCLUDE_DIRS:PATH=%s' % spec['hdf5'].prefix.include,
                '-DHDF5_LIBRARY_DIRS:PATH=%s' % spec['hdf5'].prefix.lib
            ])
        else:
            options.extend(['-DTPL_ENABLE_HDF5:BOOL=OFF'])

        if '+suite-sparse' in spec:
            options.extend([
                # FIXME: Trilinos seems to be looking for static libs only,
                # patch CMake TPL file?
                '-DTPL_ENABLE_Cholmod:BOOL=OFF',
                # '-DTPL_ENABLE_Cholmod:BOOL=ON',
                # '-DCholmod_LIBRARY_DIRS:PATH=%s' % (
                #    spec['suite-sparse'].prefix.lib,
                # '-DCholmod_INCLUDE_DIRS:PATH=%s' % (
                #    spec['suite-sparse'].prefix.include,
                '-DTPL_ENABLE_UMFPACK:BOOL=ON',
                '-DUMFPACK_LIBRARY_DIRS:PATH=%s' % (
                    spec['suite-sparse'].prefix.lib),
                '-DUMFPACK_INCLUDE_DIRS:PATH=%s' % (
                    spec['suite-sparse'].prefix.include),
                '-DUMFPACK_LIBRARY_NAMES=umfpack;amd;colamd;cholmod;' +
                'suitesparseconfig'
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_Cholmod:BOOL=OFF',
                '-DTPL_ENABLE_UMFPACK:BOOL=OFF',
            ])

        if '+metis' in spec:
            options.extend([
                '-DTPL_ENABLE_METIS:BOOL=ON',
                '-DMETIS_LIBRARY_DIRS=%s' % spec['metis'].prefix.lib,
                '-DMETIS_LIBRARY_NAMES=metis',
                '-DTPL_METIS_INCLUDE_DIRS=%s' % spec['metis'].prefix.include,
                '-DTPL_ENABLE_ParMETIS:BOOL=ON',
                '-DParMETIS_LIBRARY_DIRS=%s;%s' % (
                    spec['parmetis'].prefix.lib, spec['metis'].prefix.lib),
                '-DParMETIS_LIBRARY_NAMES=parmetis;metis',
                '-DTPL_ParMETIS_INCLUDE_DIRS=%s;%s' % (
                    spec['parmetis'].prefix.include,
                    spec['metis'].prefix.include)
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_METIS:BOOL=OFF',
                '-DTPL_ENABLE_ParMETIS:BOOL=OFF',
            ])

        if '+mumps' in spec:
            scalapack = spec['scalapack'].libs
            options.extend([
                '-DTPL_ENABLE_MUMPS:BOOL=ON',
                '-DMUMPS_LIBRARY_DIRS=%s' % spec['mumps'].prefix.lib,
                # order is important!
                '-DMUMPS_LIBRARY_NAMES=dmumps;mumps_common;pord',
                '-DTPL_ENABLE_SCALAPACK:BOOL=ON',
                '-DSCALAPACK_LIBRARY_NAMES=%s' % ';'.join(scalapack.names),
                '-DSCALAPACK_LIBRARY_DIRS=%s' % ';'.join(scalapack.directories)
            ])
            # see
            # https://github.com/trilinos/Trilinos/blob/master/packages/amesos/README-MUMPS
            cxx_flags.extend([
                '-DMUMPS_5_0'
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_MUMPS:BOOL=OFF',
                '-DTPL_ENABLE_SCALAPACK:BOOL=OFF',
            ])

        if '+superlu-dist' in spec:
            options.extend([
                '-DKokkosTSQR_ENABLE_Complex:BOOL=OFF'
            ])
            options.extend([
                '-DTPL_ENABLE_SuperLUDist:BOOL=ON',
                '-DSuperLUDist_LIBRARY_DIRS=%s' %
                spec['superlu-dist'].prefix.lib,
                '-DSuperLUDist_INCLUDE_DIRS=%s' %
                spec['superlu-dist'].prefix.include
            ])
            if spec.satisfies('^superlu-dist@4.0:'):
                options.extend([
                    '-DHAVE_SUPERLUDIST_LUSTRUCTINIT_2ARG:BOOL=ON'
                ])
        else:
            options.extend([
                '-DTPL_ENABLE_SuperLUDist:BOOL=OFF',
            ])

        if '+superlu' in spec:
            options.extend([
                '-DTPL_ENABLE_SuperLU:BOOL=ON',
                '-DSuperLU_LIBRARY_DIRS=%s' %
                spec['superlu'].prefix.lib,
                '-DSuperLU_INCLUDE_DIRS=%s' %
                spec['superlu'].prefix.include
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_SuperLU:BOOL=OFF',
            ])

        if '+pnetcdf' in spec:
            options.extend([
                '-DTPL_ENABLE_Pnetcdf:BOOL=ON',
                '-DTPL_Netcdf_Enables_Netcdf4:BOOL=ON',
                '-DTPL_Netcdf_PARALLEL:BOOL=ON',
                '-DPNetCDF_ROOT:PATH=%s' % spec['parallel-netcdf'].prefix
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_Pnetcdf:BOOL=OFF'
            ])

        if '+zlib' in spec:
            options.extend([
                '-DTPL_ENABLE_Zlib:BOOL=ON',
                '-DZlib_ROOT:PATH=%s' % spec['zlib'].prefix,
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_Zlib:BOOL=OFF'
            ])

        if '+cgns' in spec:
            options.extend([
                '-DTPL_ENABLE_CGNS:BOOL=ON',
                '-DCGNS_INCLUDE_DIRS:PATH=%s' % spec['cgns'].prefix.include,
                '-DCGNS_LIBRARY_DIRS:PATH=%s' % spec['cgns'].prefix.lib
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_CGNS:BOOL=OFF'
            ])

        options.append('-DTPL_ENABLE_ADIOS2:BOOL=' + str('+adios2' in spec))
        # ################# Miscellaneous Stuff ######################

        # OpenMP
        if '+openmp' in spec:
            options.extend([
                '-DTrilinos_ENABLE_OpenMP:BOOL=ON',
                '-DKokkos_ENABLE_OpenMP:BOOL=ON'
            ])
            if '+tpetra' in spec:
                options.extend([
                    '-DTpetra_INST_OPENMP:BOOL=ON'
                ])

        # Fortran lib
        if '+fortran' in spec:
            if spec.satisfies('%gcc') or spec.satisfies('%clang'):
                libgfortran = os.path.dirname(os.popen(
                    '%s --print-file-name libgfortran.a' %
                    join_path(mpi_bin, 'mpif90')).read())
                options.extend([
                    '-DTrilinos_EXTRA_LINK_FLAGS:STRING=-L%s/ -lgfortran' % (
                        libgfortran),
                    '-DTrilinos_ENABLE_Fortran=ON'
                ])

        float_s = 'ON' if '+float' in spec else 'OFF'
        complex_s = 'ON' if '+complex' in spec else 'OFF'
        complex_float_s = 'ON' if ('+complex' in spec and
                                   '+float' in spec) else 'OFF'
        if '+teuchos' in spec:
            options.extend([
                '-DTeuchos_ENABLE_COMPLEX=%s' % complex_s,
                '-DTeuchos_ENABLE_FLOAT=%s' % float_s
            ])

        # Explicit Template Instantiation (ETI) in Tpetra
        # NOTE: Trilinos will soon move to fixed std::uint64_t for GO and
        # std::int32_t or std::int64_t for local.
        options.append(
            '-DTrilinos_ENABLE_EXPLICIT_INSTANTIATION:BOOL=%s' % (
                'ON' if '+explicit_template_instantiation' in spec else 'OFF'
            )
        )

        if '+explicit_template_instantiation' in spec and '+tpetra' in spec:
            gotype = spec.variants['gotype'].value
            options.extend([
                '-DTpetra_INST_DOUBLE:BOOL=ON',
                '-DTpetra_INST_INT_INT:BOOL=%s' % (
                    'ON' if gotype == 'int' else 'OFF'),
                '-DTpetra_INST_INT_LONG:BOOL=%s' % (
                    'ON' if gotype == 'long' else 'OFF'),
                '-DTpetra_INST_INT_LONG_LONG:BOOL=%s' % (
                    'ON' if gotype == 'long_long' else 'OFF'),
                '-DTpetra_INST_COMPLEX_DOUBLE=%s' % complex_s,
                '-DTpetra_INST_COMPLEX_FLOAT=%s' % complex_float_s,
                '-DTpetra_INST_FLOAT=%s' % float_s,
                '-DTpetra_INST_SERIAL=ON'
            ])

        # disable due to compiler / config errors:
        if spec.satisfies('%xl') or spec.satisfies('%xl_r'):
            options.extend([
                '-DTrilinos_ENABLE_Pamgen:BOOL=OFF',
                '-DTrilinos_ENABLE_Stokhos:BOOL=OFF'
            ])

        if sys.platform == 'darwin':
            options.extend([
                '-DTrilinos_ENABLE_FEI=OFF'
            ])

        if sys.platform == 'darwin' and macos_version() >= Version('10.12'):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append('-DCMAKE_MACOSX_RPATH=ON')
        else:
            options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s' %
                           self.prefix.lib)

        if spec.satisfies('%intel') and spec.satisfies('@12.6.2'):
            # Panzer uses some std:chrono that is not recognized by Intel
            # Don't know which (maybe all) Trilinos versions this applies to
            # Don't know which (maybe all) Intel versions this applies to
            options.extend([
                '-DTrilinos_ENABLE_Panzer:BOOL=OFF'
            ])

        # collect CXX flags:
        options.extend([
            '-DCMAKE_CXX_FLAGS:STRING=%s' % (' '.join(cxx_flags)),
        ])

        # disable due to compiler / config errors:
        options.extend([
            '-DTrilinos_ENABLE_Pike=OFF'
        ])

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
