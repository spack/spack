# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


class PyNumpy(PythonPackage):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""

    homepage = "http://www.numpy.org/"
    url      = "https://pypi.io/packages/source/n/numpy/numpy-1.16.4.zip"

    install_time_test_callbacks = ['install_test', 'import_module_test']

    import_modules = [
        'numpy', 'numpy.compat', 'numpy.core', 'numpy.distutils', 'numpy.doc',
        'numpy.f2py', 'numpy.fft', 'numpy.lib', 'numpy.linalg', 'numpy.ma',
        'numpy.matrixlib', 'numpy.polynomial', 'numpy.random', 'numpy.testing',
        'numpy.distutils.command', 'numpy.distutils.fcompiler'
    ]

    version('1.16.4', sha256='7242be12a58fec245ee9734e625964b97cf7e3f2f7d016603f9e56660ce479c7')
    version('1.16.3', sha256='78a6f89da87eeb48014ec652a65c4ffde370c036d780a995edaeb121d3625621')
    version('1.16.2', sha256='6c692e3879dde0b67a9dc78f9bfb6f61c666b4562fd8619632d7043fb5b691b0')
    version('1.16.1', sha256='31d3fe5b673e99d33d70cfee2ea8fe8dccd60f265c3ed990873a88647e3dd288')
    version('1.16.0', sha256='cb189bd98b2e7ac02df389b6212846ab20661f4bafe16b5a70a6f1728c1cc7cb')
    version('1.15.4', sha256='3d734559db35aa3697dadcea492a423118c5c55d176da2f3be9c98d4803fc2a7')
    version('1.15.3', sha256='1c0c80e74759fa4942298044274f2c11b08c86230b25b8b819e55e644f5ff2b6')
    version('1.15.2', sha256='27a0d018f608a3fe34ac5e2b876f4c23c47e38295c47dd0775cc294cd2614bc1')
    version('1.15.2', sha256='27a0d018f608a3fe34ac5e2b876f4c23c47e38295c47dd0775cc294cd2614bc1')
    version('1.15.1', '898004d5be091fde59ae353e3008fe9b')
    version('1.15.0', sha256='f28e73cf18d37a413f7d5de35d024e6b98f14566a10d82100f9dc491a7d449f9')
    version('1.14.6', sha256='1250edf6f6c43e1d7823f0967416bc18258bb271dc536298eb0ea00a9e45b80a')
    version('1.14.5', sha256='a4a433b3a264dbc9aa9c7c241e87c0358a503ea6394f8737df1683c7c9a102ac')
    version('1.14.4', sha256='2185a0f31ecaa0792264fa968c8e0ba6d96acf144b26e2e1d1cd5b77fc11a691')
    version('1.14.3', '97416212c0a172db4bc6b905e9c4634b')
    version('1.14.2', '080f01a19707cf467393e426382c7619')
    version('1.14.1', 'b8324ef90ac9064cd0eac46b8b388674')
    version('1.14.0', 'c12d4bf380ac925fcdc8a59ada6c3298')
    version('1.13.3', '300a6f0528122128ac07c6deb5c95917')
    version('1.13.1', '2c3c0f4edf720c3a7b525dacc825b9ae')
    version('1.13.0', 'fd044f0b8079abeaf5e6d2e93b2c1d03')
    version('1.12.1', 'c75b072a984028ac746a6a332c209a91')
    version('1.12.0', '33e5a84579f31829bbbba084fe0a4300')
    version('1.11.3', sha256='2e0fc5248246a64628656fe14fcab0a959741a2820e003bd15538226501b82f7')
    version('1.11.2', '8308cc97be154d2f64a2387ea863c2ac')
    version('1.11.1', '5caa3428b24aaa07e72c79d115140e46')
    version('1.11.0', '19ce5c4eb16d663a0713daf0018a3021')
    version('1.10.4', '510ffc322c635511e7be95d225b6bcbb')
    version('1.9.3',  sha256='baa074bb1c7f9c822122fb81459b7caa5fc49267ca94cca69465c8dcfd63ac79')
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

        def write_library_dirs(f, dirs):
            f.write('library_dirs=%s\n' % dirs)
            if not ((platform.system() == "Darwin") and
                    (platform.mac_ver()[0] == '10.12')):
                f.write('rpath=%s\n' % dirs)

        # for build notes see http://www.scipy.org/scipylib/building/linux.html
        blas_info = []
        lapack_info = []
        lapackblas_info = []

        if '+lapack' in spec:
            lapack_info += spec['lapack'].libs

        if '+blas' in spec:
            blas_info += spec['blas'].libs

        lapackblas_info = lapack_info + blas_info

        def write_empty_libs(f, provider):
            f.write('[{0}]\n'.format(provider))
            f.write('libraries=\n')
            write_library_dirs(f, '')

        if '+blas' in spec or '+lapack' in spec:
            # note that one should not use [blas_opt] and [lapack_opt], see
            # https://github.com/numpy/numpy/commit/ffd4332262ee0295cb942c94ed124f043d801eb6
            with open('site.cfg', 'w') as f:
                # Unfortunately, numpy prefers to provide each BLAS/LAPACK
                # differently.
                blas_names  = ','.join(blas_info.names)
                blas_dirs   = ':'.join(blas_info.directories)
                lapack_names  = ','.join(lapack_info.names)
                lapack_dirs   = ':'.join(lapack_info.directories)
                lapackblas_names  = ','.join(lapackblas_info.names)
                lapackblas_dirs   = ':'.join(lapackblas_info.directories)

                handled_blas_and_lapack = False

                # Special treatment for some (!) BLAS/LAPACK. Note that
                # in this case library_dirs can not be specified within [ALL].
                if '^openblas' in spec:
                    f.write('[openblas]\n')
                    f.write('libraries=%s\n' % lapackblas_names)
                    write_library_dirs(f, lapackblas_dirs)
                    handled_blas_and_lapack = True
                else:
                    write_empty_libs(f, 'openblas')

                if '^mkl' in spec:
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
                    f.write('mkl_libs=%s\n' % 'mkl_rt')
                    write_library_dirs(f, lapackblas_dirs)
                    handled_blas_and_lapack = True
                else:
                    # Without explicitly setting the search directories to be
                    # an empty list, numpy may retrieve and use mkl libs from
                    # the system.
                    write_empty_libs(f, 'mkl')

                if '^atlas' in spec:
                    f.write('[atlas]\n')
                    f.write('atlas_libs=%s\n' % lapackblas_names)
                    write_library_dirs(f, lapackblas_dirs)
                    handled_blas_and_lapack = True
                else:
                    write_empty_libs(f, 'atlas')

                if '^netlib-lapack' in spec:
                    # netlib requires blas and lapack listed
                    # separately so that scipy can find them
                    if spec.satisfies('+blas'):
                        f.write('[blas]\n')
                        f.write('blas_libs=%s\n' % blas_names)
                        write_library_dirs(f, blas_dirs)
                    if spec.satisfies('+lapack'):
                        f.write('[lapack]\n')
                        f.write('lapack_libs=%s\n' % lapack_names)
                        write_library_dirs(f, lapack_dirs)
                    handled_blas_and_lapack = True

                if not handled_blas_and_lapack:
                    # The section title for the defaults changed in @1.10, see
                    # https://github.com/numpy/numpy/blob/master/site.cfg.example
                    if spec.satisfies('@:1.9.2'):
                        f.write('[DEFAULT]\n')
                    else:
                        f.write('[ALL]\n')
                    f.write('libraries=%s\n' % lapackblas_names)
                    write_library_dirs(f, lapackblas_dirs)

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
        # If py-numpy is installed as an external package, python won't
        # be available in the spec. See #9149 for details.
        if 'python' in self.spec:
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
