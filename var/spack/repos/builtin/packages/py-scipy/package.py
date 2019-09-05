# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScipy(PythonPackage):
    """SciPy (pronounced "Sigh Pie") is a Scientific Library for Python.
    It provides many user-friendly and efficient numerical routines such
    as routines for numerical integration and optimization."""

    homepage = "http://www.scipy.org/"
    url = "https://pypi.io/packages/source/s/scipy/scipy-1.3.1.tar.gz"

    maintainers = ['adamjstewart']
    install_time_test_callbacks = ['install_test', 'import_module_test']

    import_modules = [
        'scipy', 'scipy._build_utils', 'scipy._lib', 'scipy.cluster',
        'scipy.constants', 'scipy.fftpack', 'scipy.integrate',
        'scipy.interpolate', 'scipy.io', 'scipy.linalg', 'scipy.misc',
        'scipy.ndimage', 'scipy.odr', 'scipy.optimize', 'scipy.signal',
        'scipy.sparse', 'scipy.spatial', 'scipy.special', 'scipy.stats',
        'scipy.io.arff', 'scipy.io.harwell_boeing', 'scipy.io.matlab',
        'scipy.optimize._lsq', 'scipy.sparse.csgraph', 'scipy.sparse.linalg',
        'scipy.sparse.linalg.dsolve', 'scipy.sparse.linalg.eigen',
        'scipy.sparse.linalg.isolve', 'scipy.sparse.linalg.eigen.arpack',
        'scipy.sparse.linalg.eigen.lobpcg', 'scipy.special._precompute'
    ]

    version('1.3.1', sha256='2643cfb46d97b7797d1dbdb6f3c23fe3402904e3c90e6facfe6a9b98d808c1b5')
    version('1.3.0', sha256='c3bb4bd2aca82fb498247deeac12265921fe231502a6bc6edea3ee7fe6c40a7a')
    version('1.2.2', sha256='a4331e0b8dab1ff75d2c67b5158a8bb9a83c799d7140094dda936d876c7cfbb1')
    version('1.2.1', sha256='e085d1babcb419bbe58e2e805ac61924dac4ca45a07c9fa081144739e500aa3c')
    version('1.1.0', 'aa6bcc85276b6f25e17bcfc4dede8718')
    version('1.0.0', '53fa34bd3733a9a4216842b6000f7316')
    version('0.19.1', '6b4d91b62f1926282b127194a06b72b3')
    version('0.19.0', '91b8396231eec780222a57703d3ec550',
            url="https://pypi.io/packages/source/s/scipy/scipy-0.19.0.zip")
    version('0.18.1', '5fb5fb7ccb113ab3a039702b6c2f3327')
    version('0.17.0', '5ff2971e1ce90e762c59d2cd84837224')
    version('0.15.1', 'be56cd8e60591d6332aac792a5880110')
    version('0.15.0', '639112f077f0aeb6d80718dc5019dc7a')

    depends_on('python@2.6:2.8,3.2:')
    depends_on('python@2.7:2.8,3.4:', when='@0.18:')
    depends_on('python@3.5:', when='@1.3:')
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest', type='test')
    depends_on('py-numpy@1.5.1:+blas+lapack', type=('build', 'run'))
    depends_on('py-numpy@1.6.2:+blas+lapack', type=('build', 'run'), when='@0.16:')
    depends_on('py-numpy@1.7.1:+blas+lapack', type=('build', 'run'), when='@0.18:')
    depends_on('py-numpy@1.8.2:+blas+lapack', type=('build', 'run'), when='@0.19:')
    depends_on('py-numpy@1.13.3:+blas+lapack', type=('build', 'run'), when='@1.3:')

    # NOTE: scipy picks up Blas/Lapack from numpy, see
    # http://www.scipy.org/scipylib/building/linux.html#step-4-build-numpy-1-5-0
    depends_on('blas')
    depends_on('lapack')

    def build_args(self, spec, prefix):
        args = []

        # Build in parallel
        # Known problems with Python 3.5+
        # https://github.com/spack/spack/issues/7927
        # https://github.com/scipy/scipy/issues/7112
        if not spec.satisfies('^python@3.5:'):
            args.extend(['-j', str(make_jobs)])

        return args

    def test(self):
        # `setup.py test` is not supported.  Use one of the following
        # instead:
        #
        # - `python runtests.py`              (to build and test)
        # - `python runtests.py --no-build`   (to test installed scipy)
        # - `>>> scipy.test()`           (run tests for installed scipy
        #                                 from within an interpreter)
        pass

    def install_test(self):
        # Change directories due to the following error:
        #
        # ImportError: Error importing scipy: you should not try to import
        #       scipy from its source directory; please exit the scipy
        #       source tree, and relaunch your python interpreter from there.
        with working_dir('spack-test', create=True):
            python('-c', 'import scipy; scipy.test("full", verbose=2)')
