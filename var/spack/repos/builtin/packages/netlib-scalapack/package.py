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
import sys


class NetlibScalapack(Package):
    """ScaLAPACK is a library of high-performance linear algebra routines for
    parallel distributed memory machines
    """

    homepage = "http://www.netlib.org/scalapack/"
    url = "http://www.netlib.org/scalapack/scalapack-2.0.2.tgz"

    version('2.0.2', '2f75e600a2ba155ed9ce974a1c4b536f')
    version('2.0.1', '17b8cde589ea0423afe1ec43e7499161')
    version('2.0.0', '9e76ae7b291be27faaad47cfc256cbfe')
    # versions before 2.0.0 are not using cmake and requires blacs as
    # a separated package

    variant(
        'shared',
        default=True,
        description='Build the shared library version'
    )
    variant(
        'fpic',
        default=False,
        description='Build with -fpic compiler option'
    )

    provides('scalapack')

    depends_on('mpi')
    depends_on('lapack')
    depends_on('blas')
    depends_on('cmake', when='@2.0.0:', type='build')

    @property
    def scalapack_libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libscalapack', root=self.prefix, shared=shared, recurse=True
        )

    def install(self, spec, prefix):
        options = [
            "-DBUILD_SHARED_LIBS:BOOL=%s" % ('ON' if '+shared' in spec else
                                             'OFF'),
            "-DBUILD_STATIC_LIBS:BOOL=%s" % ('OFF' if '+shared' in spec else
                                             'ON')
        ]

        # Make sure we use Spack's Lapack:
        blas = spec['blas'].libs
        lapack = spec['lapack'].libs
        options.extend([
            '-DLAPACK_FOUND=true',
            '-DLAPACK_INCLUDE_DIRS=%s' % spec['lapack'].prefix.include,
            '-DLAPACK_LIBRARIES=%s' % (lapack.joined(';')),
            '-DBLAS_LIBRARIES=%s' % (blas.joined(';'))
        ])

        if '+fpic' in spec:
            options.extend([
                "-DCMAKE_C_FLAGS=-fPIC",
                "-DCMAKE_Fortran_FLAGS=-fPIC"
            ])

        options.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make("install")

        # The shared libraries are not installed correctly on Darwin:
        if (sys.platform == 'darwin') and ('+shared' in spec):
            fix_darwin_install_name(prefix.lib)
