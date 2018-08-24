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
import platform


class PyNumpy(PythonPackage):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""

    homepage = "http://www.numpy.org/"
    url      = "https://pypi.io/packages/source/n/numpy/numpy-1.15.1.zip"

    install_time_test_callbacks = ['install_test', 'import_module_test']

    import_modules = [
        'numpy', 'numpy.compat', 'numpy.core', 'numpy.distutils', 'numpy.doc',
        'numpy.f2py', 'numpy.fft', 'numpy.lib', 'numpy.linalg', 'numpy.ma',
        'numpy.matrixlib', 'numpy.polynomial', 'numpy.random', 'numpy.testing',
        'numpy.distutils.command', 'numpy.distutils.fcompiler'
    ]

    version('1.15.1', '898004d5be091fde59ae353e3008fe9b')
    version('1.14.3', '97416212c0a172db4bc6b905e9c4634b')
    version('1.14.2', '080f01a19707cf467393e426382c7619')
    version('1.14.1', 'b8324ef90ac9064cd0eac46b8b388674')
    version('1.14.0', 'c12d4bf380ac925fcdc8a59ada6c3298')
    version('1.13.3', '300a6f0528122128ac07c6deb5c95917')
    version('1.13.1', '2c3c0f4edf720c3a7b525dacc825b9ae')
    version('1.13.0', 'fd044f0b8079abeaf5e6d2e93b2c1d03')
    version('1.12.1', 'c75b072a984028ac746a6a332c209a91')
    version('1.12.0', '33e5a84579f31829bbbba084fe0a4300')
    version('1.11.2', '8308cc97be154d2f64a2387ea863c2ac')
    version('1.11.1', '5caa3428b24aaa07e72c79d115140e46')
    version('1.11.0', '19ce5c4eb16d663a0713daf0018a3021')
    version('1.10.4', '510ffc322c635511e7be95d225b6bcbb')
    version('1.9.2',  'e80c19d2fb25af576460bb7dac31c59a')
    version('1.9.1',  '223532d8e1bdaff5d30936439701d6e1')

    variant('blas',   default=True, description='Build with BLAS support')
    variant('lapack', default=True, description='Build with LAPACK support')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')

    depends_on('py-nose@1.0.0:', when='@:1.14', type='test')
    depends_on('py-pytest', when='@1.15:', type='test')

    def setup_dependent_package(self, module, dependent_spec):
        python_version = self.spec['python'].version.up_to(2)

        self.spec.include = join_path(
            self.prefix.lib,
            'python{0}'.format(python_version),
            'site-packages',
            'numpy/core/include')

    def patch(self):
        spec = self.spec
        # for build notes see http://www.scipy.org/scipylib/building/linux.html
        lapackblas = LibraryList('')
        if '+lapack' in spec:
            lapackblas += spec['lapack'].libs

        if '+blas' in spec:
            lapackblas += spec['blas'].libs

        if '+blas' in spec or '+lapack' in spec:
            # note that one should not use [blas_opt] and [lapack_opt], see
            # https://github.com/numpy/numpy/commit/ffd4332262ee0295cb942c94ed124f043d801eb6
            with open('site.cfg', 'w') as f:
                # Unfortunately, numpy prefers to provide each BLAS/LAPACK
                # differently.
                names  = ','.join(lapackblas.names)
                dirs   = ':'.join(lapackblas.directories)

                # Special treatment for some (!) BLAS/LAPACK. Note that
                # in this case library_dirs can not be specified within [ALL].
                if '^openblas' in spec:
                    f.write('[openblas]\n')
                    f.write('libraries=%s\n'    % names)
                elif '^mkl' in spec:
                    # numpy does not expect system libraries needed for MKL
                    # here.
                    # names = [x for x in names if x.startswith('mkl')]
                    # FIXME: as of @1.11.2, numpy does not work with separately
                    # specified threading and interface layers. A workaround is
                    # a terribly bad idea to use mkl_rt. In this case Spack
                    # will no longer be able to guarantee that one and the
                    # same variant of Blas/Lapack (32/64bit, threaded/serial)
                    # is used within the DAG. This may lead to a lot of
                    # hard-to-debug segmentation faults on user's side. Users
                    # may also break working installation by (unconsciously)
                    # setting environment variable to switch between different
                    # interface and threading layers dynamically. From this
                    # perspective it is no different from throwing away RPATH's
                    # and using LD_LIBRARY_PATH throughout Spack.
                    f.write('[mkl]\n')
                    f.write('mkl_libs=%s\n'     % 'mkl_rt')
                elif '^atlas' in spec:
                    f.write('[atlas]\n')
                    f.write('atlas_libs=%s\n'   % names)
                else:
                    # The section title for the defaults changed in @1.10, see
                    # https://github.com/numpy/numpy/blob/master/site.cfg.example
                    if spec.satisfies('@:1.9.2'):
                        f.write('[DEFAULT]\n')
                    else:
                        f.write('[ALL]\n')
                    f.write('libraries=%s\n'    % names)

                f.write('library_dirs=%s\n' % dirs)
                if not ((platform.system() == "Darwin") and
                        (platform.mac_ver()[0] == '10.12')):
                    f.write('rpath=%s\n' % dirs)

    def build_args(self, spec, prefix):
        args = []

        # From NumPy 1.10.0 on it's possible to do a parallel build.
        if self.version >= Version('1.10.0'):
            # But Parallel build in Python 3.5+ is broken.  See:
            # https://github.com/spack/spack/issues/7927
            # https://github.com/scipy/scipy/issues/7112
            if spec['python'].version < Version('3.5'):
                args = ['-j', str(make_jobs)]

        return args

    def setup_environment(self, spack_env, run_env):
        python_version = self.spec['python'].version.up_to(2)

        include_path = join_path(
            self.prefix.lib,
            'python{0}'.format(python_version),
            'site-packages',
            'numpy/core/include')

        run_env.prepend_path('CPATH', include_path)

    def test(self):
        # `setup.py test` is not supported.  Use one of the following
        # instead:
        #
        # - `python runtests.py`              (to build and test)
        # - `python runtests.py --no-build`   (to test installed numpy)
        # - `>>> numpy.test()`           (run tests for installed numpy
        #                                 from within an interpreter)
        pass

    def install_test(self):
        # Change directories due to the following error:
        #
        # ImportError: Error importing numpy: you should not try to import
        #       numpy from its source directory; please exit the numpy
        #       source tree, and relaunch your python interpreter from there.
        with working_dir('spack-test', create=True):
            python('-c', 'import numpy; numpy.test("full", verbose=2)')
