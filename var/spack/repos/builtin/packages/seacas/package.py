# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from spack import *
from spack.operating_systems.mac_os import macos_version

#
# Need to add:
#  Thread enable/disable
#  Kokkos enable/disable
#  Data Warehouse (FAODEL) enable/disable


class Seacas(CMakePackage):
    """The SEACAS Project contains the Exodus and IOSS libraries and a
     collection of applications which create, query, modify, or
     translate exodus databases.
    """
    homepage = "http://gsjaardema.github.io/seacas/"
    git      = "https://github.com/gsjaardema/seacas.git"

    maintainers = ['gsjaardema']

    # ###################### Versions ##########################

    version('master', branch='master')

    # ###################### Variants ##########################

    # Build options
    variant('fortran',      default=True,
            description='Compile with Fortran support')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=False, description='Enables MPI parallelism.')

    variant('thread_safe',  default=False,
            description='Enable thread-safe exodus and IOSS libraries')
    variant('kokkos',       default=False,
            description='Compile with Kokkos')

    # TPLs (alphabet order)
    variant('cgns',         default=True,
            description='Enable CGNS')
    variant('matio',        default=True,
            description='Compile with matio (MatLab) support')
    variant('metis',        default=False,
            description='Compile with METIS and ParMETIS')
    variant('x11',          default=True,
            description='Compile with X11')

    # Package options
    variant('allpkgs',   default=True,
            description='Compile with all packages')

    variant('algebra', default=False,
            description='Build the algebra application')
    variant('aprepro', default=False,
            description='Build aprepro')
    variant('aprepro_lib', default=False,
            description='Build the aprepro library')
    variant('blot', default=False,
            description='build the blot applications')
    variant('chaco', default=False,
            description='build the chaco library')
    variant('conjoin', default=False,
            description='build conjoin')
    variant('ejoin', default=False,
            description='build ejoin')
    variant('epu', default=False,
            description='build epu')
    variant('ex1ex2v2', default=False,
            description='build ex1ex2v2 translator')
    variant('ex2ex1v2', default=False,
            description='build ex2ex1v2 translator')
    variant('exo2mat', default=False,
            description='build exo2mat Matlab translator')
    variant('exo_format', default=False,
            description='build exo_format exodus format query')
    variant('exodiff', default=False,
            description='build exodiff')
    variant('exodus', default=False,
            description='build exodus library (C and Fortran)')
    variant('exomatlab', default=False,
            description='build exomatlab Matlab global variable translator')
    variant('exotec2', default=False,
            description='build exotec2')
    variant('exotxt', default=False,
            description='build exotxt translator')
    variant('explore', default=False,
            description='build explore (previously grope) application')
    variant('fastq', default=False,
            description='build fastq 2D mesh generator')
    variant('gen3d', default=False,
            description='build gen3d')
    variant('genshell', default=False,
            description='build genshell')
    variant('gjoin', default=False,
            description='build gjoin (use ejoin if possible)')
    variant('grepos', default=False,
            description='build grepos')
    variant('ioss', default=False,
            description='build IOSS library')
    variant('mapvar', default=False,
            description='build mapvar')
    variant('mapvar-kd', default=False,
            description='build mapvar with kd search')
    variant('mat2exo', default=False,
            description='build mat2exo Matlab translator')
    variant('nemesis', default=False,
            description='build nemesis library (deprecated)')
    variant('nemslice', default=False,
            description='build nemslice')
    variant('nemspread', default=False,
            description='build nemspread')
    variant('numbers', default=False,
            description='build numbers')
    variant('plt', default=False,
            description='build plt library')
    variant('svdi', default=False,
            description='build svdi library')
    variant('slice', default=False,
            description='build slice (experimental parallel decomposition)')
    variant('supes', default=False,
            description='build supes library (internal use)')
    variant('suplib', default=False,
            description='build suplib library (internal use)')
    variant('txtexo', default=False,
            description='build txtexo translator')

    # ###################### Dependencies ##########################

    # Everything should be compiled position independent (-fpic)

    depends_on('netcdf@4.6.2+mpi+parallel-netcdf', when='+mpi')
    depends_on('netcdf@4.6.2~mpi', when='~mpi')
    depends_on('cgns@develop+mpi+scoping', when='+cgns +mpi')
    depends_on('cgns@develop~mpi+scoping', when='+cgns ~mpi')
    depends_on('matio', when='+matio')
    depends_on('zlib', when="+zlib")

    # MPI related dependencies
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec

        cxx_flags = []
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

        options.extend([
            '-DSEACASProj_ENABLE_TESTS:BOOL=ON',
            '-DSEACASProj_ENABLE_CXX11:BOOL=ON',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),

            '-DSEACASProj_HIDE_DEPRECATED_CODE:BOOL=OFF'
        ])

        if '+allpkgs' in spec:
            options.extend([
                '-DSEACASProj_ENABLE_ALL_PACKAGES:BOOL=ON',
                '-DSEACASProj_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=ON',
                '-DSEACASProj_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON',
            ])
        else:
            options.extend([
                '-DSEACASProj_ENABLE_SEACASAlgebra:BOOL=%s' % (
                    'ON' if '+algebra' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASAprepro:BOOL=%s' % (
                    'ON' if '+aprepro' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASAprepro_lib:BOOL=%s' % (
                    'ON' if '+aprepro_lib' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASBlot:BOOL=%s' % (
                    'ON' if '+blot' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASChaco:BOOL=%s' % (
                    'ON' if '+chaco' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASConjoin:BOOL=%s' % (
                    'ON' if '+conjoin' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASEjoin:BOOL=%s' % (
                    'ON' if '+ejoin' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASEpu:BOOL=%s' % (
                    'ON' if '+epu' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASEx1ex2v2:BOOL=%s' % (
                    'ON' if '+ex1ex2v2' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASEx2ex1v2:BOOL=%s' % (
                    'ON' if '+ex2ex1v2' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExo2mat:BOOL=%s' % (
                    'ON' if '+exo2mat' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExo_format:BOOL=%s' % (
                    'ON' if '+exo_format' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExodiff:BOOL=%s' % (
                    'ON' if '+exodiff' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExodus:BOOL=%s' % (
                    'ON' if '+exodus' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExodus_for:BOOL=%s' % (
                    'ON' if '+exodus' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExoIIv2for32:BOOL=%s' % (
                    'ON' if '+exodus' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExomatlab:BOOL=%s' % (
                    'ON' if '+exomatlab' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExotec2:BOOL=%s' % (
                    'ON' if '+exotec2' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExotxt:BOOL=%s' % (
                    'ON' if '+exotxt' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExplore:BOOL=%s' % (
                    'ON' if '+explore' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASFastq:BOOL=%s' % (
                    'ON' if '+fastq' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASGen3D:BOOL=%s' % (
                    'ON' if '+gen3d' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASGenshell:BOOL=%s' % (
                    'ON' if '+genshell' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASGjoin:BOOL=%s' % (
                    'ON' if '+gjoin' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASGrepos:BOOL=%s' % (
                    'ON' if '+grepos' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASIoss:BOOL=%s' % (
                    'ON' if '+ioss' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASMapvar:BOOL=%s' % (
                    'ON' if '+mapvar' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASMapvar-kd:BOOL=%s' % (
                    'ON' if '+mapvar-kd' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASMapvarlib:BOOL=%s' % (
                    'ON' if '+mapvar' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASMapvarlib:BOOL=%s' % (
                    'ON' if '+mapvar-kd' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASMat2exo:BOOL=%s' % (
                    'ON' if '+mat2exo' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASNemesis:BOOL=%s' % (
                    'ON' if '+nemesis' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASNemslice:BOOL=%s' % (
                    'ON' if '+nemslice' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASNemspread:BOOL=%s' % (
                    'ON' if '+nemspread' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASNumbers:BOOL=%s' % (
                    'ON' if '+numbers' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASPLT:BOOL=%s' % (
                    'ON' if '+plt' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASSVDI:BOOL=%s' % (
                    'ON' if '+svdi' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASSlice:BOOL=%s' % (
                    'ON' if '+slice' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASSupes:BOOL=%s' % (
                    'ON' if '+supes' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASSuplib:BOOL=%s' % (
                    'ON' if '+suplib' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASSuplibC:BOOL=%s' % (
                    'ON' if '+suplib' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASSuplibCpp:BOOL=%s' % (
                    'ON' if '+suplib' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASTxtexo:BOOL=%s' % (
                    'ON' if '+txtexo' in spec else 'OFF'),
            ])

        if '+kokkos' in spec:
            if '+openmp' in spec:
                options.extend([
                    '-DKokkos_ENABLE_OpenMP:BOOL=ON'
                ])

            if '+cuda' in spec:
                options.extend([
                    '-DSEACASProj_ENABLE_Kokkos:BOOL=ON',
                    '-DTPL_ENABLE_CUDA:Bool=ON',
                    '-DCUDA_TOOLKIT_ROOT_DIR:PATH=${CUDA_PATH}',
                    '-DKOKKOS_ENABLE_DEPRECATED_CODE:BOOL=OFF',
                    '-DKokkos_ENABLE_Pthread:BOOL=OFF',
                ])
            else:
                options.extend([
                    '-DSEACASProj_ENABLE_Kokkos:BOOL=ON',
                    '-DSEACASProj_ENABLE_OpenMP:Bool=ON',
                    '-DKOKKOS_ENABLE_DEPRECATED_CODE:BOOL=OFF',
                    '-DKokkos_ENABLE_Pthread:BOOL=OFF',
                ])
        else:
            options.extend([
                '-DSEACASProj_ENABLE_Kokkos:BOOL=OFF'
            ])

        if '+thread_safe' in spec:
            options.extend([
                '-DSEACASExodus_ENABLE_THREADSAFE:BOOL=ON',
                '-DSEACASIoss_ENABLE_THREADSAFE:BOOL=ON',
            ])

        # ######################### TPLs #############################

        # Note: -DXYZ_LIBRARY_NAMES= needs semicolon separated list of names
        options.extend([
            '-DTPL_ENABLE_Netcdf:BOOL=ON',
            '-DNetCDF_ROOT:PATH=%s' % spec['netcdf'].prefix,
            '-DTPL_ENABLE_X11:BOOL=%s' % (
                'ON' if '+x11' in spec else 'OFF'),
        ])

        if '+hdf5' in spec:
            options.extend([
                '-DTPL_ENABLE_HDF5:BOOL=ON',
                '-DHDF5_INCLUDE_DIRS:PATH=%s' % spec['hdf5'].prefix.include,
                '-DHDF5_LIBRARY_DIRS:PATH=%s' % spec['hdf5'].prefix.lib
            ])
        else:
            options.extend(['-DTPL_ENABLE_HDF5:BOOL=OFF'])

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

        if '+mpi' in spec:
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

        if '+matio' in spec:
            options.extend([
                '-DTPL_ENABLE_Matio:BOOL=ON',
                '-DMatio_ROOT:PATH=%s' % spec['matio'].prefix
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_Matio:BOOL=OFF'
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
                '-DCGNS_ROOT:PATH=%s' % spec['cgns'].prefix,
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_CGNS:BOOL=OFF'
            ])

        # ################# Miscellaneous Stuff ######################

        # Fortran lib
        if '+fortran' in spec:
            options.extend([
                '-DSEACASProj_ENABLE_Fortran=ON'
            ])

        if '~fortran' in spec:
            options.extend([
                '-DSEACASProj_ENABLE_Fortran=OFF'
            ])

        if sys.platform == 'darwin' and macos_version() >= Version('10.12'):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append('-DCMAKE_MACOSX_RPATH:BOOL=ON')
        else:
            options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s' %
                           self.prefix.lib)

        # collect CXX flags:
        options.extend([
            '-DCMAKE_CXX_FLAGS:STRING=%s' % (' '.join(cxx_flags)),
        ])

        return options
