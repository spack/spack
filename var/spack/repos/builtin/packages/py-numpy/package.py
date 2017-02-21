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
import os
import platform


class PyNumpy(PythonPackage):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""

    homepage = "http://www.numpy.org/"
    url      = "https://pypi.io/packages/source/n/numpy/numpy-1.9.1.tar.gz"

    version('1.12.0', '33e5a84579f31829bbbba084fe0a4300',
            url="https://pypi.io/packages/source/n/numpy/numpy-1.12.0.zip")
    version('1.11.2', '03bd7927c314c43780271bf1ab795ebc')
    version('1.11.1', '2f44a895a8104ffac140c3a70edbd450')
    version('1.11.0', 'bc56fb9fc2895aa4961802ffbdb31d0b')
    version('1.10.4', 'aed294de0aa1ac7bd3f9745f4f1968ad')
    version('1.9.2',  'a1ed53432dbcd256398898d35bc8e645')
    version('1.9.1',  '78842b73560ec378142665e712ae4ad9')

    variant('blas',   default=True, description='Build with BLAS support')
    variant('lapack', default=True, description='Build with LAPACK support')

    depends_on('python@2.7:2.8,3.4:')
    depends_on('py-setuptools', type='build')
    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')

    patch('intelcompiler-1.12.patch', when='@1.12.0%intel')

    def setup_dependent_package(self, module, dep_spec):
        python_version = self.spec['python'].version.up_to(2)
        arch = '{0}-{1}'.format(platform.system().lower(), platform.machine())

        self.spec.include = join_path(
            self.prefix.lib,
            'python{0}'.format(python_version),
            'site-packages',
            'numpy-{0}-py{1}-{2}.egg'.format(
                self.spec.version, python_version, arch),
            'numpy/core/include')

    def patch(self):
        spec = self.spec

        if spec.satisfies('%intel@16:'):
            # Intel 16 replaced -openmp with -qopenmp
            # This change prevents thousands of lines of deprecation warnings
            filter_file('-openmp', self.compiler.openmp_flag,
                        'numpy/distutils/intelccompiler.py', string=True)
            filter_file('-openmp', self.compiler.openmp_flag,
                        'numpy/distutils/fcompiler/intel.py', string=True)

        # The following patches are only necessary for BLAS/LAPACK support
        if '+blas' not in spec and '+lapack' not in spec:
            return

        lapackblas_includes  = set()
        lapackblas_libraries = LibraryList('')
        if '+lapack' in spec:
            lapackblas_includes.add(spec['lapack'].prefix.include)
            lapackblas_libraries += spec['lapack'].lapack_libs

        if '+blas' in spec:
            lapackblas_includes.add(spec['blas'].prefix.include)
            lapackblas_libraries += spec['blas'].blas_libs

        # Each BLAS/LAPACK requires a custom site.cfg

        # Generic build notes (very out-of-date):
        # http://www.scipy.org/scipylib/building/linux.html

        # Example site.cfg:
        # https://github.com/numpy/numpy/blob/master/site.cfg.example
        with open('site.cfg', 'w') as f:
            libraries = ','.join(lapackblas_libraries.names)

            if '^openblas' in spec:
                f.write('[openblas]\n')
                f.write('libraries = {0}\n'.format(libraries))

            elif '^mkl' in spec:
                # Intel MKL build notes:
                # https://software.intel.com/en-us/articles/numpyscipy-with-intel-mkl

                # library_dirs are in compilers_and_libraries_2017/linux/mkl/lib/intel64  # noqa
                # include_dirs are in compilers_and_libraries_2017/linux/mkl/include      # noqa
                lapackblas_includes = set()
                for libdir in lapackblas_libraries.directories:
                    incdir = os.path.dirname(os.path.dirname(libdir))
                    incdir = join_path(incdir, 'include')
                    lapackblas_includes.add(incdir)

                f.write('[mkl]\n')
                f.write('mkl_libs = {0}\n'.format('mkl_rt'))
                f.write('lapack_libs = \n')

            elif '^atlas' in spec:
                f.write('[atlas]\n')
                f.write('atlas_libs = {0}\n'.format(libraries))

            else:
                # The section title for the defaults changed in @1.10
                if spec.satisfies('@1.10:'):
                    f.write('[ALL]\n')
                else:
                    f.write('[DEFAULT]\n')
                f.write('libraries = {0}\n'.format(libraries))

            include_dirs = os.pathsep.join(lapackblas_includes)
            library_dirs = os.pathsep.join(lapackblas_libraries.directories)

            f.write('include_dirs = {0}\n'.format(include_dirs))
            f.write('library_dirs = {0}\n'.format(library_dirs))

            # macOS 10.12 does not support RPATHs
            if not ((platform.system() == "Darwin") and
                    (platform.mac_ver()[0] == '10.12')):
                f.write('rpath = {0}\n'.format(library_dirs))

    def build_args(self, spec, prefix):
        args = []

        # From NumPy 1.10.0 on it's possible to do a parallel build
        if self.version >= Version('1.10.0'):
            args.extend(['-j', str(make_jobs)])

        if self.compiler.name == 'intel':
            if spec.satisfies('target=x86_64'):
                args.extend(['--compiler=intelem', '--fcompiler=intelem'])
            else:
                args.extend(['--compiler=intel', '--fcompiler=intel'])

        return args
