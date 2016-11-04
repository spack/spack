##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Dealii(CMakePackage):
    """C++ software library providing well-documented tools to build finite
    element codes for a broad variety of PDEs."""
    homepage = "https://www.dealii.org"
    url      = "https://github.com/dealii/dealii/releases/download/v8.4.1/dealii-8.4.1.tar.gz"

    # Don't add RPATHs to this package for the full build DAG.
    # only add for immediate deps.
    transitive_rpaths = False

    version('8.4.2', '84c6bd3f250d3e0681b645d24cb987a7')
    version('8.4.1', 'efbaf16f9ad59cfccad62302f36c3c1d')
    version('8.4.0', 'ac5dbf676096ff61e092ce98c80c2b00')
    version('8.3.0', 'fc6cdcb16309ef4bea338a4f014de6fa')
    version('8.2.1', '71c728dbec14f371297cd405776ccf08')
    version('8.1.0', 'aa8fadc2ce5eb674f44f997461bf668d')
    version('develop', git='https://github.com/dealii/dealii.git')

    variant('mpi',      default=True,  description='Compile with MPI')
    variant('arpack',   default=True,
            description='Compile with Arpack and PArpack (only with MPI)')
    variant('doc',      default=False,
            description='Compile with documentation')
    variant('gsl',      default=True,  description='Compile with GSL')
    variant('hdf5',     default=True,
            description='Compile with HDF5 (only with MPI)')
    variant('metis',    default=True,  description='Compile with Metis')
    variant('netcdf',   default=True,
            description='Compile with Netcdf (only with MPI)')
    variant('oce',      default=True,  description='Compile with OCE')
    variant('p4est',    default=True,
            description='Compile with P4est (only with MPI)')
    variant('petsc',    default=True,
            description='Compile with Petsc (only with MPI)')
    variant('slepc',    default=True,
            description='Compile with Slepc (only with Petsc and MPI)')
    variant('trilinos', default=True,
            description='Compile with Trilinos (only with MPI)')
    variant('python',   default=True,
            description='Compile with Python bindings')

    # required dependencies, light version
    depends_on("blas")
    # Boost 1.58 is blacklisted, see
    # https://github.com/dealii/dealii/issues/1591
    # Require at least 1.59
    # +python won't affect @:8.4.2
    depends_on("boost@1.59.0:+thread+system+serialization+iostreams",
               when='@:8.4.2~mpi')
    depends_on("boost@1.59.0:+thread+system+serialization+iostreams+mpi",
               when='@:8.4.2+mpi')
    # since @8.5.0: (and @develop) python bindings are introduced:
    depends_on("boost@1.59.0:+thread+system+serialization+iostreams",
               when='@8.5.0:~mpi~python')
    depends_on("boost@1.59.0:+thread+system+serialization+iostreams+mpi",
               when='@8.5.0:+mpi~python')
    depends_on("boost@1.59.0:+thread+system+serialization+iostreams+python",
               when='@8.5.0:~mpi+python')
    depends_on(
        "boost@1.59.0:+thread+system+serialization+iostreams+mpi+python",
        when='@8.5.0:+mpi+python')
    depends_on("bzip2")
    depends_on("cmake", type='build')
    depends_on("lapack")
    depends_on("muparser")
    depends_on("suite-sparse")
    depends_on("tbb")
    depends_on("zlib")

    # optional dependencies
    depends_on("mpi",              when="+mpi")
    depends_on("arpack-ng+mpi",    when='+arpack+mpi')
    depends_on("doxygen+graphviz", when='+doc')
    depends_on("graphviz",         when='+doc')
    depends_on("gsl",              when='@8.5.0:+gsl')
    depends_on("hdf5+mpi",         when='+hdf5+mpi')
    depends_on("metis@5:",         when='+metis')
    depends_on("netcdf+mpi",       when="+netcdf+mpi")
    depends_on("netcdf-cxx",       when='+netcdf+mpi')
    depends_on("oce",              when='+oce')
    depends_on("p4est",            when='+p4est+mpi')
    depends_on("petsc+mpi",        when='@8.4.2:+petsc+mpi')
    depends_on('python',           when='@8.5.0:+python')
    depends_on("slepc",            when='@8.4.2:+slepc+petsc+mpi')
    depends_on("petsc@:3.6.4+mpi", when='@:8.4.1+petsc+mpi')
    depends_on("slepc@:3.6.3",     when='@:8.4.1+slepc+petsc+mpi')
    depends_on("trilinos",         when='+trilinos+mpi')

    # developer dependnecies
    depends_on("numdiff",     when='@develop')
    depends_on("astyle@2.04", when='@develop')

    def cmake_args(self):
        spec = self.spec
        options = []
        options.extend(std_cmake_args)

        # CMAKE_BUILD_TYPE should be DebugRelease | Debug | Release
        for word in options[:]:
            if word.startswith('-DCMAKE_BUILD_TYPE'):
                options.remove(word)

        lapack_blas = spec['lapack'].lapack_libs + spec['blas'].blas_libs
        options.extend([
            '-DCMAKE_BUILD_TYPE=DebugRelease',
            '-DDEAL_II_COMPONENT_EXAMPLES=ON',
            '-DDEAL_II_WITH_THREADS:BOOL=ON',
            '-DBOOST_DIR=%s' % spec['boost'].prefix,
            '-DBZIP2_DIR=%s' % spec['bzip2'].prefix,
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

        # MPI
        if '+mpi' in spec:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=ON',
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=OFF',
            ])

        # Optional dependencies for which librariy names are the same as CMake
        # variables:
        for library in (
                'gsl', 'hdf5', 'p4est', 'petsc', 'slepc', 'trilinos', 'metis'):
            if library in spec:
                options.extend([
                    '-D%s_DIR=%s' % (library.upper(), spec[library].prefix),
                    '-DDEAL_II_WITH_%s:BOOL=ON' % library.upper()
                ])
            else:
                options.extend([
                    '-DDEAL_II_WITH_%s:BOOL=OFF' % library.upper()
                ])

        # doxygen
        options.extend([
            '-DDEAL_II_COMPONENT_DOCUMENTATION=%s' %
            ('ON' if '+doc' in spec else 'OFF'),
        ])

        # arpack
        if '+arpack' in spec:
            options.extend([
                '-DARPACK_DIR=%s' % spec['arpack-ng'].prefix,
                '-DDEAL_II_WITH_ARPACK=ON',
                '-DDEAL_II_ARPACK_WITH_PARPACK=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_ARPACK=OFF'
            ])

        # since Netcdf is spread among two, need to do it by hand:
        if '+netcdf' in spec:
            options.extend([
                '-DNETCDF_FOUND=true',
                '-DNETCDF_LIBRARIES=%s;%s' % (
                    join_path(spec['netcdf-cxx'].prefix.lib,
                              'libnetcdf_c++.%s' % dso_suffix),
                    join_path(spec['netcdf'].prefix.lib,
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

        return options

    def setup_environment(self, spack_env, env):
        env.set('DEAL_II_DIR', self.prefix)
