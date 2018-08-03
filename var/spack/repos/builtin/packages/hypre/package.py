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
import os
import sys


class Hypre(Package):
    """Hypre is a library of high performance preconditioners that
       features parallel multigrid methods for both structured and
       unstructured grid problems."""

    homepage = "http://computation.llnl.gov/project/linear_solvers/software.php"
    url      = "https://github.com/LLNL/hypre/archive/v2.14.0.tar.gz"
    git      = "https://github.com/LLNL/hypre.git"

    version('develop', branch='master')
    version('2.14.0', 'ecde5cc807ec45bfb647e9f28d2eaea1')
    version('2.13.0', '4b688a5c15b6b5e3de5e045ae081b89b')
    version('2.12.1', 'c6fcb6d7e57cec1c7ce4a44da885068c')
    version('2.11.2', 'd507943a1a3ce5681c3308e2f3a6dd34')
    version('2.11.1', '3f02ef8fd679239a6723f60b7f796519')
    version('2.10.1', 'dc048c4cabb3cd549af72591474ad674')
    version('2.10.0b', '768be38793a35bb5d055905b271f5b8e')
    version('xsdk-0.2.0', tag='xsdk-0.2.0')

    # hypre does not know how to build shared libraries on Darwin
    variant('shared', default=(sys.platform != 'darwin'),
            description="Build shared library (disables static library)")
    # SuperluDist have conflicting headers with those in Hypre
    variant('internal-superlu', default=True,
            description="Use internal Superlu routines")
    variant('int64', default=False,
            description="Use 64bit integers")
    variant('mpi', default=True, description='Enable MPI support')

    # Patch to add ppc64le in config.guess
    patch('ibm-ppc64le.patch', when='@:2.11.1')

    depends_on("mpi", when='+mpi')
    depends_on("blas")
    depends_on("lapack")

    def url_for_version(self, version):
        if version >= Version('2.12.0'):
            url = 'https://github.com/LLNL/hypre/archive/v{0}.tar.gz'
        else:
            url = 'http://computation.llnl.gov/project/linear_solvers/download/hypre-{0}.tar.gz'

        return url.format(version)

    def install(self, spec, prefix):
        # Note: --with-(lapack|blas)_libs= needs space separated list of names
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs

        configure_args = [
            '--prefix=%s' % prefix,
            '--with-lapack-libs=%s' % ' '.join(lapack.names),
            '--with-lapack-lib-dirs=%s' % ' '.join(lapack.directories),
            '--with-blas-libs=%s' % ' '.join(blas.names),
            '--with-blas-lib-dirs=%s' % ' '.join(blas.directories)
        ]

        if '+mpi' in self.spec:
            os.environ['CC'] = spec['mpi'].mpicc
            os.environ['CXX'] = spec['mpi'].mpicxx
            os.environ['F77'] = spec['mpi'].mpif77
            configure_args.append('--with-MPI')
        else:
            configure_args.append('--without-MPI')

        if '+int64' in self.spec:
            configure_args.append('--enable-bigint')

        if '+shared' in self.spec:
            configure_args.append("--enable-shared")

        if '~internal-superlu' in self.spec:
            configure_args.append("--without-superlu")
            # MLI and FEI do not build without superlu on Linux
            configure_args.append("--without-mli")
            configure_args.append("--without-fei")

        # Hypre's source is staged under ./src so we'll have to manually
        # cd into it.
        with working_dir("src"):
            configure(*configure_args)

            make()
            if self.run_tests:
                make("check")
                make("test")
                Executable(join_path('test', 'ij'))()
                sstruct = Executable(join_path('test', 'struct'))
                sstruct()
                sstruct('-in', 'test/sstruct.in.default', '-solver', '40',
                        '-rhsone')
            make("install")

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
