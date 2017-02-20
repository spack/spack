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
from spack.spec import UnsupportedCompilerError


class Elemental(CMakePackage):
    """Elemental: Distributed-memory dense and sparse-direct linear algebra 
       and optimization library."""

    homepage = "http://libelemental.org"
    url      = "https://github.com/elemental/Elemental/archive/v0.87.6.tar.gz"

    version('0.87.7', '6c1e7442021c59a36049e37ea69b8075')
    version('0.87.6', '9fd29783d45b0a0e27c0df85f548abe9')

    variant('debug', default=False, 
            description='Builds a debug version of the libraries')
    variant('shared', default=True, 
            description='Enables the build of shared libraries')
    variant('hybrid', default=True, 
            description='Make use of OpenMP within MPI packing/unpacking')
    variant('openmp_blas', default=False,
            description='Use OpenMP for threading in the BLAS library')
    variant('c', default=False, 
            description='Build C interface')
    variant('python', default=False, 
            description='Install Python interface')
    variant('parmetis', default=False, 
            description='Enable ParMETIS')
    variant('quad', default=False, 
            description='Enable quad precision')
    variant('int64', default=False, 
            description='Use 64bit integers')
    # When this variant is set remove the normal dependencies since
    # Elemental has to build BLAS and ScaLAPACK internally
    variant('int64_blas', default=False, 
            description='Use 64bit integers for BLAS.' 
            ' Requires local build of BLAS library.')
    variant('scalapack', default=False,
            description='Build with ScaLAPACK library')

    depends_on('cmake', type='build')
    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on('blas', when='~openmp_blas ~int64_blas')
    # Hack to forward variant to openblas package
    # Allow Elemental to build internally when using 8-byte ints
    depends_on('openblas +openmp', when='+openmp_blas ~int64_blas')
    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on('lapack', when='~openmp_blas')
    depends_on('metis')
    depends_on('metis +int64', when='+int64')
    depends_on('mpi')
    # Allow Elemental to build internally when using 8-byte ints
    depends_on('scalapack', when='+scalapack ~int64_blas')
    extends('python', when='+python')
    depends_on('python@:2.8', when='+python')

    @property
    def elemental_libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            ['libEl'], root=self.prefix, shared=shared, recurse=True
        )

    def build_type(self):
        """Returns the correct value for the ``CMAKE_BUILD_TYPE`` variable
        :return: value for ``CMAKE_BUILD_TYPE``
        """
        if '+debug' in self.spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        spec = self.spec

        if '@:0.87.7' in spec and '%intel@:17.0.2' in spec:
            raise UnsupportedCompilerError(
                "Elemental {0} has a known bug with compiler: {1} {2}".format(
                    spec.version, spec.compiler.name, spec.compiler.version))

        args = [
            '-DCMAKE_INSTALL_MESSAGE:STRING=LAZY',
            '-DEL_PREFER_OPENBLAS:BOOL=TRUE',
            '-DEL_DISABLE_SCALAPACK:BOOL=%s'   % ('~scalapack' in spec),
            '-DGFORTRAN_LIB=libgfortran.so',
            '-DBUILD_SHARED_LIBS:BOOL=%s'      % ('+shared' in spec),
            '-DEL_HYBRID:BOOL=%s'              % ('+hybrid' in spec),
            '-DEL_C_INTERFACE:BOOL=%s'         % ('+c' in spec),
            '-DINSTALL_PYTHON_PACKAGE:BOOL=%s' % ('+python' in spec),
            '-DEL_DISABLE_PARMETIS:BOOL=%s'    % ('~parmetis' in spec),
            '-DEL_DISABLE_QUAD:BOOL=%s'        % ('~quad' in spec),
            '-DEL_USE_64BIT_INTS:BOOL=%s'      % ('+int64' in spec),
            '-DEL_USE_64BIT_BLAS_INTS:BOOL=%s' % ('+int64_blas' in spec)]

        # If using 64bit int BLAS libraries, elemental has to build
        # them internally
        if '+int64_blas' in spec:
            args.extend(['-DEL_BLAS_SUFFIX:STRING={0}'.format((
                '_64_' if '+int64_blas' in spec else '_')),
                '-DCUSTOM_BLAS_SUFFIX:BOOL=TRUE']),
            if '+scalapack' in spec:
                args.extend(['-DEL_LAPACK_SUFFIX:STRING={0}'.format((
                    '_64_' if '+int64_blas' in spec else '_')),
                    '-DCUSTOM_LAPACK_SUFFIX:BOOL=TRUE']),
        else:
            math_libs = (spec['lapack'].lapack_libs +
                         spec['blas'].blas_libs)

            if '+scalapack' in spec:
                math_libs = spec['scalapack'].scalapack_libs + math_libs

            args.extend([
                '-DMATH_LIBS:STRING={0}'.format(math_libs.search_flags),
                '-DMATH_LIBS:STRING={0}'.format(math_libs.link_flags)])

        if '+python' in spec:
            args.extend([
                '-DPYTHON_SITE_PACKAGES:STRING={0}'.format(site_packages_dir)])

        return args
