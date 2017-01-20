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
import platform


class PyNumpy(PythonPackage):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""

    homepage = "http://www.numpy.org/"
    url      = "https://pypi.io/packages/source/n/numpy/numpy-1.9.1.tar.gz"

    import_modules = [
        'numpy', 'numpy.compat', 'numpy.core', 'numpy.distutils', 'numpy.doc',
        'numpy.f2py', 'numpy.fft', 'numpy.lib', 'numpy.linalg', 'numpy.ma',
        'numpy.matrixlib', 'numpy.polynomial', 'numpy.random', 'numpy.testing',
        'numpy.distutils.command', 'numpy.distutils.fcompiler'
    ]

    # FIXME: numpy._build_utils and numpy.core.code_generators failed to import
    # FIXME: Is this expected?

    version('1.12.0', '33e5a84579f31829bbbba084fe0a4300',
            url="https://pypi.python.org/packages/b7/9d/8209e555ea5eb8209855b6c9e60ea80119dab5eff5564330b35aa5dc4b2c/numpy-1.12.0.zip")
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

    # Tests require:
    # TODO: Add a 'test' deptype
    # depends_on('py-nose@1.0.0:', type='test')

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
        # for build notes see http://www.scipy.org/scipylib/building/linux.html
        lapackblas = LibraryList('')
        if '+lapack' in spec:
            lapackblas += spec['lapack'].lapack_libs

        if '+blas' in spec:
            lapackblas += spec['blas'].blas_libs

        if '+blas' in spec or '+lapack' in spec:
            with open('site.cfg', 'w') as f:
                f.write('[DEFAULT]\n')
                f.write('libraries=%s\n'    % ','.join(lapackblas.names))
                f.write('library_dirs=%s\n' % ':'.join(lapackblas.directories))
                if not ((platform.system() == "Darwin") and
                        (platform.mac_ver()[0] == '10.12')):
                    f.write('rpath=%s\n' % ':'.join(lapackblas.directories))

    def build_args(self, spec, prefix):
        args = []

        # From NumPy 1.10.0 on it's possible to do a parallel build
        if self.version >= Version('1.10.0'):
            args = ['-j', str(make_jobs)]

        return args

    def test(self, spec, prefix):
        # `setup.py test` is not supported.  Use one of the following
        # instead:
        #
        # - `python runtests.py`              (to build and test)
        # - `python runtests.py --no-build`   (to test installed numpy)
        # - `>>> numpy.test()`           (run tests for installed numpy
        #                                 from within an interpreter)
        pass

    @PythonPackage.sanity_check('install')
    @PythonPackage.on_package_attributes(run_tests=True)
    def install_test(self):
        # Change directories due to the following error:
        #
        # ImportError: Error importing numpy: you should not try to import
        #       numpy from its source directory; please exit the numpy
        #       source tree, and relaunch your python interpreter from there.
        with working_dir('..'):
            python('-c', 'import numpy; numpy.test("full", verbose=2)')
