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
    url      = "https://pypi.io/packages/source/n/numpy/numpy-1.17.2.zip"

    maintainers = ['adamjstewart']
    install_time_test_callbacks = ['install_test', 'import_module_test']

    import_modules = [
        'numpy', 'numpy.compat', 'numpy.core', 'numpy.distutils', 'numpy.doc',
        'numpy.f2py', 'numpy.fft', 'numpy.lib', 'numpy.linalg', 'numpy.ma',
        'numpy.matrixlib', 'numpy.polynomial', 'numpy.random', 'numpy.testing',
        'numpy.distutils.command', 'numpy.distutils.fcompiler'
    ]

    version('1.17.2', sha256='73615d3edc84dd7c4aeb212fa3748fb83217e00d201875a47327f55363cef2df')
    version('1.17.1', sha256='f11331530f0eff69a758d62c2461cd98cdc2eae0147279d8fc86e0464eb7e8ca')
    version('1.17.0', sha256='951fefe2fb73f84c620bec4e001e80a80ddaa1b84dce244ded7f1e0cbe0ed34a')
    version('1.16.5', sha256='8bb452d94e964b312205b0de1238dd7209da452343653ab214b5d681780e7a0c')
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
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@1.16:')
    depends_on('python@3.5:', type=('build', 'run'), when='@1.17:')
    depends_on('py-setuptools', type='build')
    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')

    depends_on('py-nose@1.0.0:', when='@:1.14', type='test')
    depends_on('py-pytest', when='@1.15:', type='test')

    # Allows you to specify order of BLAS/LAPACK preference
    # https://github.com/numpy/numpy/pull/13132
    patch('blas-lapack-order.patch', when='@1.15:1.16')

    # GCC 4.8 is the minimum version that works
    conflicts('%gcc@:4.7', msg='GCC 4.8+ required')

    def flag_handler(self, name, flags):
        # -std=c99 at least required, old versions of GCC default to -std=c90
        if self.spec.satisfies('%gcc@:5.1') and name == 'cflags':
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)

    @run_before('build')
    def set_blas_lapack(self):
        # https://numpy.org/devdocs/user/building.html
        # https://github.com/numpy/numpy/blob/master/site.cfg.example

        # Skip if no BLAS/LAPACK requested
        spec = self.spec
        if '+blas' not in spec and '+lapack' not in spec:
            return

        def write_library_dirs(f, dirs):
            f.write('library_dirs = {0}\n'.format(dirs))
            if not ((platform.system() == 'Darwin') and
                    (Version(platform.mac_ver()[0]).up_to(2) == Version(
                        '10.12'))):
                f.write('rpath = {0}\n'.format(dirs))

        blas_libs = LibraryList([])
        blas_headers = HeaderList([])
        if '+blas' in spec:
            blas_libs = spec['blas'].libs
            blas_headers = spec['blas'].headers

        lapack_libs = LibraryList([])
        lapack_headers = HeaderList([])
        if '+lapack' in spec:
            lapack_libs = spec['lapack'].libs
            lapack_headers = spec['lapack'].headers

        lapackblas_libs = lapack_libs + blas_libs
        lapackblas_headers = lapack_headers + blas_headers

        blas_lib_names   = ','.join(blas_libs.names)
        blas_lib_dirs    = ':'.join(blas_libs.directories)
        blas_header_dirs = ':'.join(blas_headers.directories)

        lapack_lib_names   = ','.join(lapack_libs.names)
        lapack_lib_dirs    = ':'.join(lapack_libs.directories)
        lapack_header_dirs = ':'.join(lapack_headers.directories)

        lapackblas_lib_names   = ','.join(lapackblas_libs.names)
        lapackblas_lib_dirs    = ':'.join(lapackblas_libs.directories)
        lapackblas_header_dirs = ':'.join(lapackblas_headers.directories)

        # Tell numpy where to find BLAS/LAPACK libraries
        with open('site.cfg', 'w') as f:
            if '^intel-mkl' in spec or '^intel-parallel-studio+mkl' in spec:
                f.write('[mkl]\n')
                # FIXME: as of @1.11.2, numpy does not work with separately
                # specified threading and interface layers. A workaround is a
                # terribly bad idea to use mkl_rt. In this case Spack will no
                # longer be able to guarantee that one and the same variant of
                # Blas/Lapack (32/64bit, threaded/serial) is used within the
                # DAG. This may lead to a lot of hard-to-debug segmentation
                # faults on user's side. Users may also break working
                # installation by (unconsciously) setting environment variable
                # to switch between different interface and threading layers
                # dynamically. From this perspective it is no different from
                # throwing away RPATH's and using LD_LIBRARY_PATH throughout
                # Spack.
                f.write('libraries = {0}\n'.format('mkl_rt'))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^blis' in spec:
                f.write('[blis]\n')
                f.write('libraries = {0}\n'.format(blas_lib_names))
                write_library_dirs(f, blas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(blas_header_dirs))

            if '^openblas' in spec:
                f.write('[openblas]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^libflame' in spec:
                f.write('[flame]\n')
                f.write('libraries = {0}\n'.format(lapack_lib_names))
                write_library_dirs(f, lapack_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapack_header_dirs))

            if '^atlas' in spec:
                f.write('[atlas]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)
                f.write('include_dirs = {0}\n'.format(lapackblas_header_dirs))

            if '^veclibfort' in spec:
                f.write('[accelerate]\n')
                f.write('libraries = {0}\n'.format(lapackblas_lib_names))
                write_library_dirs(f, lapackblas_lib_dirs)

            if '^netlib-lapack' in spec:
                # netlib requires blas and lapack listed
                # separately so that scipy can find them
                if spec.satisfies('+blas'):
                    f.write('[blas]\n')
                    f.write('libraries = {0}\n'.format(blas_lib_names))
                    write_library_dirs(f, blas_lib_dirs)
                    f.write('include_dirs = {0}\n'.format(blas_header_dirs))
                if spec.satisfies('+lapack'):
                    f.write('[lapack]\n')
                    f.write('libraries = {0}\n'.format(lapack_lib_names))
                    write_library_dirs(f, lapack_lib_dirs)
                    f.write('include_dirs = {0}\n'.format(lapack_header_dirs))

    def setup_environment(self, spack_env, run_env):
        # Tell numpy which BLAS/LAPACK libraries we want to use.
        # https://github.com/numpy/numpy/pull/13132
        # https://numpy.org/devdocs/user/building.html#accelerated-blas-lapack-libraries
        spec = self.spec

        # https://numpy.org/devdocs/user/building.html#blas
        if '~blas' in spec:
            blas = ''
        elif spec['blas'].name == 'intel-mkl' or \
                spec['blas'].name == 'intel-parallel-studio':
            blas = 'mkl'
        elif spec['blas'].name == 'blis':
            blas = 'blis'
        elif spec['blas'].name == 'openblas':
            blas = 'openblas'
        elif spec['blas'].name == 'atlas':
            blas = 'atlas'
        elif spec['blas'].name == 'veclibfort':
            blas = 'accelerate'
        else:
            blas = 'blas'

        spack_env.set('NPY_BLAS_ORDER', blas)

        # https://numpy.org/devdocs/user/building.html#lapack
        if '~lapack' in spec:
            lapack = ''
        elif spec['lapack'].name == 'intel-mkl' or \
                spec['lapack'].name == 'intel-parallel-studio':
            lapack = 'mkl'
        elif spec['lapack'].name == 'openblas':
            lapack = 'openblas'
        elif spec['lapack'].name == 'libflame':
            lapack = 'flame'
        elif spec['lapack'].name == 'atlas':
            lapack = 'atlas'
        elif spec['lapack'].name == 'veclibfort':
            lapack = 'accelerate'
        else:
            lapack = 'lapack'

        spack_env.set('NPY_LAPACK_ORDER', lapack)

    def build_args(self, spec, prefix):
        args = []

        # From NumPy 1.10.0 on it's possible to do a parallel build.
        # https://numpy.org/devdocs/user/building.html#parallel-builds
        if self.version >= Version('1.10.0'):
            # But Parallel build in Python 3.5+ is broken.  See:
            # https://github.com/spack/spack/issues/7927
            # https://github.com/scipy/scipy/issues/7112
            if spec['python'].version < Version('3.5'):
                args = ['-j', str(make_jobs)]

        return args

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
