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
import os
from spack import *
from spack.spec import UnsupportedCompilerError


class Elemental(CMakePackage):
    """Elemental: Distributed-memory dense and sparse-direct linear algebra
       and optimization library."""

    homepage = "http://libelemental.org"
    url      = "https://github.com/elemental/Elemental/archive/v0.87.7.tar.gz"
    git      = "https://github.com/elemental/Elemental.git"

    version('develop', branch='master')
    version('0.87.7', '6c1e7442021c59a36049e37ea69b8075')
    version('0.87.6', '9fd29783d45b0a0e27c0df85f548abe9')

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
    variant('cublas', default=False,
            description='Enable cuBLAS for local BLAS operations')
    # When this variant is set remove the normal dependencies since
    # Elemental has to build BLAS and ScaLAPACK internally
    variant('int64_blas', default=False,
            description='Use 64bit integers for BLAS.'
            ' Requires local build of BLAS library.')
    variant('scalapack', default=False,
            description='Build with ScaLAPACK library')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('blas', default='openblas', values=('openblas', 'mkl', 'accelerate', 'essl'),
            description='Enable the use of OpenBlas/MKL/Accelerate/ESSL')
    variant('mpfr', default=False,
            description='Support GNU MPFR\'s'
            'arbitrary-precision floating-point arithmetic')

    # Note that #1712 forces us to enumerate the different blas variants
    depends_on('blas', when='~openmp_blas ~int64_blas')
    # Hack to forward variant to openblas package
    depends_on('openblas', when='blas=openblas ~openmp_blas ~int64_blas')
    # Allow Elemental to build internally when using 8-byte ints
    depends_on('openblas threads=openmp', when='blas=openblas +openmp_blas ~int64_blas')

    depends_on('intel-mkl', when="blas=mkl ~openmp_blas ~int64_blas")
    depends_on('intel-mkl threads=openmp', when='blas=mkl +openmp_blas ~int64_blas')
    depends_on('intel-mkl@2017.1 +openmp +ilp64', when='blas=mkl +openmp_blas +int64_blas')

    depends_on('veclibfort', when='blas=accelerate')

    depends_on('essl ~cuda', when='blas=essl ~openmp_blas ~int64_blas')
    depends_on('essl threads=openmp', when='blas=essl +openmp_blas ~int64_blas')

    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on('lapack', when='blas=openblas ~openmp_blas')
    depends_on('netlib-lapack +external-blas', when='blas=essl')

    depends_on('metis')
    depends_on('metis +int64', when='+int64')
    depends_on('mpi')
    # Allow Elemental to build internally when using 8-byte ints
    depends_on('scalapack', when='+scalapack ~int64_blas')
    extends('python', when='+python')
    depends_on('python@:2.8', when='+python')
    depends_on('gmp', when='+mpfr')
    depends_on('mpc', when='+mpfr')
    depends_on('mpfr', when='+mpfr')

    patch('elemental_cublas.patch', when='+cublas')
    patch('cmake_0.87.7.patch', when='@0.87.7')

    @property
    def libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libEl', root=self.prefix, shared=shared, recursive=True
        )

    def cmake_args(self):
        spec = self.spec

        if '@:0.87.7' in spec and '%intel@:17.0.2' in spec:
            raise UnsupportedCompilerError(
                "Elemental {0} has a known bug with compiler: {1} {2}".format(
                    spec.version, spec.compiler.name, spec.compiler.version))

        args = [
            '-DCMAKE_INSTALL_MESSAGE:STRING=LAZY',
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DEL_PREFER_OPENBLAS:BOOL=TRUE',
            '-DEL_DISABLE_SCALAPACK:BOOL=%s'   % ('~scalapack' in spec),
            '-DBUILD_SHARED_LIBS:BOOL=%s'      % ('+shared' in spec),
            '-DEL_HYBRID:BOOL=%s'              % ('+hybrid' in spec),
            '-DEL_C_INTERFACE:BOOL=%s'         % ('+c' in spec),
            '-DINSTALL_PYTHON_PACKAGE:BOOL=%s' % ('+python' in spec),
            '-DEL_DISABLE_PARMETIS:BOOL=%s'    % ('~parmetis' in spec),
            '-DEL_DISABLE_QUAD:BOOL=%s'        % ('~quad' in spec),
            '-DEL_USE_64BIT_INTS:BOOL=%s'      % ('+int64' in spec),
            '-DEL_USE_64BIT_BLAS_INTS:BOOL=%s' % ('+int64_blas' in spec),
            '-DEL_DISABLE_MPFR:BOOL=%s'        % ('~mpfr' in spec)]

        if self.spec.satisfies('%intel'):
            ifort = env['SPACK_F77']
            intel_bin = os.path.dirname(ifort)
            intel_root = os.path.dirname(intel_bin)
            libfortran = find_libraries('libifcoremt',
                                        root=intel_root, recursive=True)
        elif self.spec.satisfies('%gcc'):
            # see <stage_folder>/debian/rules as an example:
            mpif77 = Executable(spec['mpi'].mpif77)
            libfortran = LibraryList(mpif77('--print-file-name',
                                            'libgfortran.%s' % dso_suffix,
                                            output=str).strip())
        elif self.spec.satisfies('%xl') or self.spec.satisfies('%xl_r'):
            xl_fort = env['SPACK_F77']
            xl_bin = os.path.dirname(xl_fort)
            xl_root = os.path.dirname(xl_bin)
            libfortran = find_libraries('libxlf90_r',
                                        root=xl_root, recursive=True)
        else:
            libfortran = None

        if libfortran:
            args.append('-DGFORTRAN_LIB=%s' % libfortran.libraries[0])

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
            math_libs = (spec['lapack'].libs +
                         spec['blas'].libs)

            if '+scalapack' in spec:
                math_libs = spec['scalapack'].libs + math_libs

            args.extend([
                '-DMATH_LIBS:STRING={0}'.format(math_libs.ld_flags)])

        if '+python' in spec:
            args.extend([
                '-DPYTHON_SITE_PACKAGES:STRING={0}'.format(site_packages_dir)])

        return args
