##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import os


class Dealii(CMakePackage):
    """C++ software library providing well-documented tools to build finite
    element codes for a broad variety of PDEs."""
    homepage = "https://www.dealii.org"
    url = "https://github.com/dealii/dealii/releases/download/v8.4.1/dealii-8.4.1.tar.gz"

    maintainers = ['davydden', 'jppelteret']

    # Don't add RPATHs to this package for the full build DAG.
    # only add for immediate deps.
    transitive_rpaths = False

    version('8.5.1', '39b9ebd6ab083d63cfc9044319aaa2ee')
    version('8.5.0', 'ef999cc310b007559a6343bf5b1759bc')
    version('8.4.2', '84c6bd3f250d3e0681b645d24cb987a7')
    version('8.4.1', 'efbaf16f9ad59cfccad62302f36c3c1d')
    version('8.4.0', 'ac5dbf676096ff61e092ce98c80c2b00')
    version('8.3.0', 'fc6cdcb16309ef4bea338a4f014de6fa')
    version('8.2.1', '71c728dbec14f371297cd405776ccf08')
    version('8.1.0', 'aa8fadc2ce5eb674f44f997461bf668d')
    version('develop', git='https://github.com/dealii/dealii.git', branch='master')

    variant('mpi',      default=True,  description='Compile with MPI')
    variant('assimp',   default=False,
            description='Compile with Assimp')
    variant('arpack',   default=True,
            description='Compile with Arpack and PArpack (only with MPI)')
    variant('adol-c',   default=False,
            description='Compile with Adol-c')
    variant('doc',      default=False,
            description='Compile with documentation')
    variant('gsl',      default=True,  description='Compile with GSL')
    variant('hdf5',     default=True,
            description='Compile with HDF5 (only with MPI)')
    variant('metis',    default=True,  description='Compile with Metis')
    variant('nanoflann', default=False, description='Compile with Nanoflann')
    variant('netcdf',   default=True,
            description='Compile with Netcdf (only with MPI)')
    variant('oce',      default=True,  description='Compile with OCE')
    variant('p4est',    default=True,
            description='Compile with P4est (only with MPI)')
    variant('petsc',    default=True,
            description='Compile with Petsc (only with MPI)')
    variant('sundials', default=False,
            description='Compile with Sundials')
    variant('slepc',    default=True,
            description='Compile with Slepc (only with Petsc and MPI)')
    variant('trilinos', default=True,
            description='Compile with Trilinos (only with MPI)')
    variant('python',   default=True,
            description='Compile with Python bindings')
    variant('int64',    default=False,
            description='Compile with 64 bit indices support')
    variant('optflags', default=False,
            description='Compile using additional optimization flags')
    variant('build_type', default='DebugRelease',
            description='The build type to build',
            values=('Debug', 'Release', 'DebugRelease'))
    variant('cuda', default=False,
            description='Build with CUDA')

    # required dependencies, light version
    depends_on("blas")
    # Boost 1.58 is blacklisted, see
    # https://github.com/dealii/dealii/issues/1591
    # Require at least 1.59
    # +python won't affect @:8.4.2
    # FIXME: once concretizer can unite unconditional and
    # conditional dependencies, simplify to:
    # depends_on("boost@1.59.0+thread+system+serialization+iostreams")
    # depends_on("boost+mpi", when='+mpi')
    # depends_on("boost+python", when='+python')
    depends_on("boost@1.59.0:1.63,1.66:+thread+system+serialization+iostreams",
               when='@:8.4.2~mpi')
    depends_on("boost@1.59.0:1.63,1.66:+thread+system+serialization+iostreams+mpi",
               when='@:8.4.2+mpi')
    # since @8.5.0: (and @develop) python bindings are introduced:
    depends_on("boost@1.59.0:1.63,1.66:+thread+system+serialization+iostreams",
               when='@8.5.0:~mpi~python')
    depends_on("boost@1.59.0:1.63,1.66:+thread+system+serialization+iostreams+mpi",
               when='@8.5.0:+mpi~python')
    depends_on("boost@1.59.0:1.63,1.66:+thread+system+serialization+iostreams+python",
               when='@8.5.0:~mpi+python')
    depends_on("boost@1.59.0:1.63,1.66:+thread+system+serialization+iostreams+mpi+python",
               when='@8.5.0:+mpi+python')
    # bzip2 is not needed since 9.0
    depends_on("bzip2", when='@:8.99')
    depends_on("lapack")
    depends_on("muparser")
    depends_on("suite-sparse")
    depends_on("tbb")
    depends_on("zlib")

    # optional dependencies
    depends_on("mpi",              when="+mpi")
    depends_on("adol-c@2.6.4:",    when='@9.0:+adol-c')
    depends_on("arpack-ng+mpi",    when='+arpack+mpi')
    depends_on("assimp",           when='@9.0:+assimp')
    depends_on("doxygen+graphviz", when='+doc')
    depends_on("graphviz",         when='+doc')
    depends_on("gsl",              when='@8.5.0:+gsl')
    depends_on("hdf5+mpi",         when='+hdf5+mpi')
    depends_on("cuda@8:",          when='+cuda')
    depends_on("cmake@3.9:",       when='+cuda')
    # FIXME: concretizer bug. The two lines mimic what comes from PETSc
    # but we should not need it
    depends_on("metis@5:+int64+real64",   when='+metis+int64')
    depends_on("metis@5:~int64+real64",   when='+metis~int64')
    depends_on("nanoflann",        when="@9.0:+nanoflann")
    depends_on("netcdf+mpi",       when="+netcdf+mpi")
    depends_on("netcdf-cxx",       when='+netcdf+mpi')
    depends_on("oce",              when='+oce')
    depends_on("p4est",            when='+p4est+mpi')
    depends_on("petsc+mpi~int64",  when='+petsc+mpi~int64')
    depends_on("petsc+mpi+int64",  when='+petsc+mpi+int64')
    depends_on("petsc@:3.6.4",     when='@:8.4.1+petsc+mpi')
    depends_on('python',           when='@8.5.0:+python')
    depends_on("slepc",            when='+slepc+petsc+mpi')
    depends_on("slepc@:3.6.3",     when='@:8.4.1+slepc+petsc+mpi')
    depends_on("slepc~arpack",     when='+slepc+petsc+mpi+int64')
    depends_on("sundials~pthread", when='@9.0:+sundials')
    depends_on("trilinos+amesos+aztec+epetra+ifpack+ml+muelu+sacado+teuchos",       when='+trilinos+mpi~int64')
    depends_on("trilinos+amesos+aztec+epetra+ifpack+ml+muelu+sacado+teuchos~hypre", when="+trilinos+mpi+int64")

    # check that the combination of variants makes sense
    conflicts('+assimp', when='@:8.5.1')
    conflicts('+nanoflann', when='@:8.5.1')
    conflicts('+sundials', when='@:8.5.1')
    conflicts('+adol-c', when='@:8.5.1')
    conflicts('+gsl',    when='@:8.4.2')
    conflicts('+python', when='@:8.4.2')
    conflicts('+cuda', when='%gcc@6:')
    for p in ['+arpack', '+hdf5', '+netcdf', '+p4est', '+petsc',
              '+slepc', '+trilinos']:
        conflicts(p, when='~mpi')

    def cmake_args(self):
        spec = self.spec
        options = []
        # release flags
        cxx_flags_release = []
        # debug and release flags
        cxx_flags = []

        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        options.extend([
            '-DDEAL_II_COMPONENT_EXAMPLES=ON',
            '-DDEAL_II_WITH_THREADS:BOOL=ON',
            '-DBOOST_DIR=%s' % spec['boost'].prefix,
            # CMake's FindBlas/Lapack may pickup system's blas/lapack instead
            # of Spack's. Be more specific to avoid this.
            # Note that both lapack and blas are provided in -DLAPACK_XYZ.
            '-DLAPACK_FOUND=true',
            '-DLAPACK_INCLUDE_DIRS=%s;%s' % (
                spec['lapack'].prefix.include, spec['blas'].prefix.include),
            '-DLAPACK_LIBRARIES=%s' % lapack_blas.joined(';'),
            '-DMUPARSER_DIR=%s' % spec['muparser'].prefix,
            '-DUMFPACK_DIR=%s' % spec['suite-sparse'].prefix,
            '-DTBB_DIR=%s' % spec['tbb'].prefix,
            '-DZLIB_DIR=%s' % spec['zlib'].prefix
        ])

        if spec.satisfies('@:8.99'):
            options.extend([
                # Cmake may still pick up system's bzip2, fix this:
                '-DBZIP2_FOUND=true',
                '-DBZIP2_INCLUDE_DIRS=%s' % spec['bzip2'].prefix.include,
                '-DBZIP2_LIBRARIES=%s' % spec['bzip2'].libs.joined(';')
            ])

        # Set recommended flags for maximum (matrix-free) performance, see
        # https://groups.google.com/forum/?fromgroups#!topic/dealii/3Yjy8CBIrgU
        if spec.satisfies('%gcc'):
            cxx_flags_release.extend(['-O3'])
            cxx_flags.extend(['-march=native'])
        elif spec.satisfies('%intel'):
            cxx_flags_release.extend(['-O3'])
            cxx_flags.extend(['-march=native'])
        elif spec.satisfies('%clang'):
            cxx_flags_release.extend(['-O3', '-ffp-contract=fast'])
            cxx_flags.extend(['-march=native'])

        # Python bindings
        if spec.satisfies('@8.5.0:'):
            options.extend([
                '-DDEAL_II_COMPONENT_PYTHON_BINDINGS=%s' %
                ('ON' if '+python' in spec else 'OFF')
            ])

        # Set directory structure:
        if spec.satisfies('@:8.2.1'):
            options.extend(['-DDEAL_II_COMPONENT_COMPAT_FILES=OFF'])
        else:
            options.extend([
                '-DDEAL_II_EXAMPLES_RELDIR=share/deal.II/examples',
                '-DDEAL_II_DOCREADME_RELDIR=share/deal.II/',
                '-DDEAL_II_DOCHTML_RELDIR=share/deal.II/doc'
            ])

        # CUDA
        # FIXME  -DDEAL_II_CUDA_FLAGS="-arch=sm_60"
        if '+cuda' in spec:
            options.extend([
                '-DDEAL_II_WITH_CUDA=ON',
                '-DDEAL_II_WITH_CXX14=OFF'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_CUDA=OFF',
            ])

        # MPI
        if '+mpi' in spec:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=ON',
                '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=OFF',
            ])

        # Optional dependencies for which library names are the same as CMake
        # variables:
        for library in (
                'gsl', 'hdf5', 'p4est', 'petsc', 'slepc', 'trilinos', 'metis',
                'sundials', 'nanoflann'):
            if library in spec:
                options.extend([
                    '-D%s_DIR=%s' % (library.upper(), spec[library].prefix),
                    '-DDEAL_II_WITH_%s:BOOL=ON' % library.upper()
                ])
            else:
                options.extend([
                    '-DDEAL_II_WITH_%s:BOOL=OFF' % library.upper()
                ])

        # adol-c
        if '+adol-c' in spec:
            options.extend([
                '-DADOLC_DIR=%s' % spec['adol-c'].prefix,
                '-DDEAL_II_WITH_ADOLC=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_ADOLC=OFF'
            ])

        # doxygen
        options.extend([
            '-DDEAL_II_COMPONENT_DOCUMENTATION=%s' %
            ('ON' if '+doc' in spec else 'OFF'),
        ])

        # arpack
        if '+arpack' in spec and '+mpi' in spec:
            options.extend([
                '-DARPACK_DIR=%s' % spec['arpack-ng'].prefix,
                '-DDEAL_II_WITH_ARPACK=ON',
                '-DDEAL_II_ARPACK_WITH_PARPACK=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_ARPACK=OFF'
            ])

        # Assimp
        if '+assimp' in spec:
            options.extend([
                '-DDEAL_II_WITH_ASSIMP=ON',
                '-DASSIMP_DIR=%s' % spec['assimp'].prefix
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_ASSIMP=OFF'
            ])

        # since Netcdf is spread among two, need to do it by hand:
        if '+netcdf' in spec and '+mpi' in spec:
            # take care of lib64 vs lib installed lib locations:
            if os.path.isdir(spec['netcdf-cxx'].prefix.lib):
                netcdfcxx_lib_dir = spec['netcdf-cxx'].prefix.lib
            else:
                netcdfcxx_lib_dir = spec['netcdf-cxx'].prefix.lib64
            if os.path.isdir(spec['netcdf'].prefix.lib):
                netcdf_lib_dir = spec['netcdf'].prefix.lib
            else:
                netcdf_lib_dir = spec['netcdf'].prefix.lib64

            options.extend([
                '-DNETCDF_FOUND=true',
                '-DNETCDF_LIBRARIES=%s;%s' % (
                    join_path(netcdfcxx_lib_dir,
                              'libnetcdf_c++.%s' % dso_suffix),
                    join_path(netcdf_lib_dir,
                              'libnetcdf.%s' % dso_suffix)),
                '-DNETCDF_INCLUDE_DIRS=%s;%s' % (
                    spec['netcdf-cxx'].prefix.include,
                    spec['netcdf'].prefix.include),
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_NETCDF=OFF'
            ])

        # Open Cascade
        if '+oce' in spec:
            options.extend([
                '-DOPENCASCADE_DIR=%s' % spec['oce'].prefix,
                '-DDEAL_II_WITH_OPENCASCADE=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_OPENCASCADE=OFF'
            ])

        # 64 bit indices
        options.extend([
            '-DDEAL_II_WITH_64BIT_INDICES=%s' % ('+int64' in spec)
        ])

        # collect CXX flags:
        if len(cxx_flags_release) > 0 and '+optflags' in spec:
            options.extend([
                '-DCMAKE_CXX_FLAGS_RELEASE:STRING=%s' % (
                    ' '.join(cxx_flags_release)),
                '-DCMAKE_CXX_FLAGS:STRING=%s' % (
                    ' '.join(cxx_flags))
            ])

        return options

    def setup_environment(self, spack_env, run_env):
        run_env.set('DEAL_II_DIR', self.prefix)
