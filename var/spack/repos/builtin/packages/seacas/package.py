# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *

#
# Need to add:
#  KOKKOS support using an external (i.e. spack-supplied) kokkos library.
#  Data Warehouse (FAODEL) enable/disable


class Seacas(CMakePackage):
    """The SEACAS Project contains the Exodus and IOSS libraries and a
     collection of applications which create, query, modify, or
     translate exodus databases.  Default is to build the exodus and
     IOSS libraries and the io_shell, io_info, io_modify, struc_to_unstruc apps.
    """
    homepage = "https://gsjaardema.github.io/seacas/"
    git      = "https://github.com/gsjaardema/seacas.git"
    url      = "https://github.com/gsjaardema/seacas/archive/v2019-08-20.tar.gz"
    maintainers = ['gsjaardema']

    # ###################### Versions ##########################
    version('master', branch='master')
    version('2022-03-04', sha256='a934a473e1fdfbc8dbb55058358551a02e03a60e5cdbf2b28b8ecd3d9500bfa5')
    version('2022-01-27', sha256='beff12583814dcaf75cf8f1a78bb183c1dcc8937bc18d5206672e3a692db05e0')
    version('2021-09-30', sha256='5d061e35e93eb81214da3b67ddda2829cf5efed38a566be6363a9866ba2f9ab3')
    version('2021-05-12', sha256='92663767f0317018d6f6e422e8c687e49f6f7eb2b92e49e837eb7dc0ca0ac33d')
    version('2021-04-05', sha256='76f66eec1fec7aba30092c94c7609495e6b90d9dcb6f35b3ee188304d02c6e04')
    version('2021-01-20', sha256='7814e81981d03009b6816be3eb4ed3845fd02cc69e006ee008a2cbc85d508246')
    version('2021-01-06', sha256='b233502a7dc3e5ab69466054cf358eb033e593b8679c6721bf630b03999bd7e5')
    version('2020-08-13', sha256='e5eaf203eb2dbfb33c61ccde26deea459d058aaea79b0847e2f4bdb0cef1ddcb')
    version('2020-05-12', sha256='7fc6915f60568b36e052ba07a77d691c99abe42eaba6ae8a6dc74bb33490ed60')
    version('2020-03-16', sha256='2eb404f3dcb17c3e7eacf66978372830d40ef3722788207741fcd48417807af6')
    version('2020-01-16', sha256='5ae84f61e410a4f3f19153737e0ac0493b144f20feb1bbfe2024f76613d8bff5')
    version('2019-12-18', sha256='f82cfa276ebc5fe6054852383da16eba7a51c81e6640c73b5f01fc3109487c6f')
    version('2019-10-14', sha256='ca4cf585cdbc15c25f302140fe1f61ee1a30d72921e032b9a854492b6c61fb91')
    version('2019-08-20', sha256='a82c1910c2b37427616dc3716ca0b3c1c77410db6723aefb5bea9f47429666e5')
    version('2019-07-26', sha256='651dac832b0cfee0f63527f563415c8a65b8e4d79242735c1e2aec606f6b2e17')

    # ###################### Variants ##########################
    # Package options
    # The I/O libraries (exodus, IOSS) are always built
    # -- required of both applications and legacy variants.
    variant('applications', default=True,
            description='Build all "current" SEACAS applications. This'
            ' includes a debatable list of essential applications: '
            'aprepro, conjoin, cpup, ejoin, epu, exo2mat, mat2exo, '
            'exo_format, exodiff, explore, grepos, io_shell, io_info, '
            'io_modify, nemslice, nemspread, zellij')
    variant('legacy', default=True,
            description='Build all "legacy" SEACAS applications. This includes'
            ' a debatable list of "legacy" applications: algebra, blot, '
            'exomatlab, exotxt, fastq, gen3d, genshell, gjoin, mapvar, '
            'mapvar-kd, numbers, txtexo, nemesis')

    # Build options
    variant('fortran',      default=True,
            description='Compile with Fortran support')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Enables MPI parallelism.')

    variant('thread_safe',  default=False,
            description='Enable thread-safe exodus and IOSS libraries')

    # TPLs (alphabet order)
    variant('adios2',       default=False,
            description='Enable ADIOS2')
    variant('cgns',         default=True,
            description='Enable CGNS')
    variant('faodel',       default=False,
            description='Enable Faodel')
    variant('matio',        default=True,
            description='Compile with matio (MatLab) support')
    variant('metis',        default=False,
            description='Compile with METIS and ParMETIS')
    variant('x11',          default=True,
            description='Compile with X11')

    # ###################### Dependencies ##########################

    # Everything should be compiled position independent (-fpic)

    depends_on('netcdf-c@4.8.0:+mpi+parallel-netcdf', when='+mpi')
    depends_on('netcdf-c@4.8.0:~mpi', when='~mpi')
    depends_on('hdf5+hl~mpi', when='~mpi')
    depends_on('cgns@4.2.0:+mpi+scoping', when='+cgns +mpi')
    depends_on('cgns@4.2.0:~mpi+scoping', when='+cgns ~mpi')
    depends_on('fmt@8.1.0:', when='@2022-03-04:')

    with when('+adios2'):
        depends_on('adios2@master')
        depends_on('adios2~mpi', when='~mpi')
        depends_on('adios2+mpi', when='+mpi')

    depends_on('matio', when='+matio')
    with when('+metis'):
        depends_on('metis+int64+real64')
        depends_on('parmetis+int64', when='+mpi')
    depends_on('libx11', when='+x11')

    # The Faodel TPL is only supported in seacas@2021-04-05:
    depends_on('faodel@1.2108.1:+mpi', when='+faodel +mpi')
    depends_on('faodel@1.2108.1:~mpi', when='+faodel ~mpi')
    conflicts('+faodel', when='@:2021-01-20', msg='The Faodel TPL is only compatible with @2021-04-05 and later.')

    # MPI related dependencies
    depends_on('mpi', when='+mpi')

    depends_on('cmake@3.1:', type='build')

    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix.lib)

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant

        options = []

        # #################### Base Settings #######################

        if '+mpi' in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                '-DTPL_ENABLE_MPI:BOOL=ON',
                '-DMPI_BASE_DIR:PATH=%s'      % spec['mpi'].prefix,
            ])
        else:
            '-DTPL_ENABLE_MPI:BOOL=OFF'

        options.extend([
            '-DSEACASProj_ENABLE_TESTS:BOOL=ON',
            '-DSEACASProj_ENABLE_CXX11:BOOL=ON',
            from_variant('CMAKE_INSTALL_RPATH_USE_LINK_PATH', 'shared'),
            from_variant('BUILD_SHARED_LIBS', 'shared'),
            '-DSEACASProj_ENABLE_Kokkos:BOOL=OFF',
            '-DSEACASProj_HIDE_DEPRECATED_CODE:BOOL=OFF',
            from_variant('SEACASExodus_ENABLE_THREADSAFE', 'thread_safe'),
            from_variant('SEACASIoss_ENABLE_THREADSAFE', 'thread_safe'),
            from_variant('SEACASProj_ENABLE_Fortran', 'fortran'),
            from_variant('TPL_ENABLE_X11', 'x11'),
        ])

        # ########## What applications should be built #############
        # Check whether they want everything; if so, do the easy way...
        if '+applications' in spec and '+legacy' in spec:
            options.extend([
                '-DSEACASProj_ENABLE_ALL_PACKAGES:BOOL=ON',
                '-DSEACASProj_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=ON',
                '-DSEACASProj_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON',
            ])
        else:
            # Don't want everything; handle the subsets:
            options.extend([
                '-DSEACASProj_ENABLE_ALL_PACKAGES:BOOL=OFF',
                '-DSEACASProj_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF',
                '-DSEACASProj_ENABLE_SECONDARY_TESTED_CODE:BOOL=OFF',
                '-DSEACASProj_ENABLE_SEACASIoss:BOOL=ON',
                '-DSEACASProj_ENABLE_SEACASExodus:BOOL=ON',
                from_variant('SEACASProj_ENABLE_SEACASExodus_for', 'fortran'),
                from_variant('SEACASProj_ENABLE_SEACASExoIIv2for32', 'fortran'),
            ])

            if '+applications' in spec:
                options.extend([
                    '-DSEACASProj_ENABLE_SEACASAprepro:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASAprepro_lib:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASConjoin:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASCpup:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASEjoin:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASEpu:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASExo2mat:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASExo_format:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASExodiff:BOOL=ON',
                    from_variant('SEACASProj_ENABLE_SEACASExplore', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASGrepos', 'fortran'),
                    '-DSEACASProj_ENABLE_SEACASMat2exo:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASNas2exo:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASNemslice:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASNemspread:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASSlice:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASZellij:BOOL=ON',
                ])

            if '+legacy' in spec:
                options.extend([
                    from_variant('SEACASProj_ENABLE_SEACASAlgebra', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASBlot', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASEx1ex2v2', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASEx2ex1v2', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASExomatlab', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASExotec2', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASExotxt', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASFastq', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASGen3D', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASGenshell', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASGjoin', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASMapvar', 'fortran'),
                    '-DSEACASProj_ENABLE_SEACASMapvar-kd:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASNemesis:BOOL=ON',
                    from_variant('SEACASProj_ENABLE_SEACASNumbers', 'fortran'),
                    from_variant('SEACASProj_ENABLE_SEACASTxtexo', 'fortran'),
                ])

        # ##################### Dependencies ##########################
        # Always need NetCDF-C
        options.extend([
            '-DTPL_ENABLE_Netcdf:BOOL=ON',
            '-DNetCDF_ROOT:PATH=%s' % spec['netcdf-c'].prefix,
        ])

        if '+parmetis' in spec:
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
        elif '+metis' in spec:
            options.extend([
                '-DTPL_ENABLE_METIS:BOOL=ON',
                '-DMETIS_LIBRARY_DIRS=%s' % spec['metis'].prefix.lib,
                '-DMETIS_LIBRARY_NAMES=metis',
                '-DTPL_METIS_INCLUDE_DIRS=%s' % spec['metis'].prefix.include,
                '-DTPL_ENABLE_ParMETIS:BOOL=OFF',
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_METIS:BOOL=OFF',
                '-DTPL_ENABLE_ParMETIS:BOOL=OFF',
            ])

        if '+matio' in spec:
            options.extend([
                '-DTPL_ENABLE_Matio:BOOL=ON',
                '-DMatio_ROOT:PATH=%s' % spec['matio'].prefix
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_Matio:BOOL=OFF'
            ])

        if '+cgns' in spec:
            options.extend([
                '-DTPL_ENABLE_CGNS:BOOL=ON',
                '-DCGNS_ROOT:PATH=%s' % spec['cgns'].prefix,
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_CGNS:BOOL=OFF'
            ])

        define = CMakePackage.define
        from_variant = self.define_from_variant
        options.append(from_variant('TPL_ENABLE_Faodel', 'faodel'))

        for pkg in ('Faodel', 'BOOST'):
            if pkg.lower() in spec:
                options.append(define(pkg + '_ROOT', spec[pkg.lower()].prefix))

        if '+adios2' in spec:
            options.extend([
                '-DTPL_ENABLE_ADIOS2:BOOL=ON',
                '-DADIOS2_ROOT:PATH=%s' % spec['adios2'].prefix,
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_ADIOS2:BOOL=OFF'
            ])

        # ################# RPath Handling ######################
        if sys.platform == 'darwin' and macos_version() >= Version('10.12'):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append('-DCMAKE_MACOSX_RPATH:BOOL=ON')
        else:
            options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s' %
                           self.prefix.lib)

        return options
