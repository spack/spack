# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScipy(PythonPackage):
    """SciPy (pronounced "Sigh Pie") is a Scientific Library for Python.
    It provides many user-friendly and efficient numerical routines such
    as routines for numerical integration and optimization."""

    homepage = "https://www.scipy.org/"
    url      = "https://pypi.io/packages/source/s/scipy/scipy-1.4.1.tar.gz"

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

    version('1.4.1',  sha256='dee1bbf3a6c8f73b6b218cb28eed8dd13347ea2f87d572ce19b289d6fd3fbc59')
    version('1.4.0',  sha256='31f7cfa93b01507c935c12b535e24812594002a02a56803d7cd063e9920d25e8')
    version('1.3.3',  sha256='64bf4e8ae0db2d42b58477817f648d81e77f0b381d0ea4427385bba3f959380a')
    version('1.3.2',  sha256='a03939b431994289f39373c57bbe452974a7da724ae7f9620a1beee575434da4')
    version('1.3.1',  sha256='2643cfb46d97b7797d1dbdb6f3c23fe3402904e3c90e6facfe6a9b98d808c1b5')
    version('1.3.0',  sha256='c3bb4bd2aca82fb498247deeac12265921fe231502a6bc6edea3ee7fe6c40a7a')
    version('1.2.3',  sha256='ecbe6413ca90b8e19f8475bfa303ac001e81b04ec600d17fa7f816271f7cca57')
    version('1.2.2',  sha256='a4331e0b8dab1ff75d2c67b5158a8bb9a83c799d7140094dda936d876c7cfbb1')
    version('1.2.1',  sha256='e085d1babcb419bbe58e2e805ac61924dac4ca45a07c9fa081144739e500aa3c')
    version('1.1.0',  sha256='878352408424dffaa695ffedf2f9f92844e116686923ed9aa8626fc30d32cfd1')
    version('1.0.0',  sha256='87ea1f11a0e9ec08c264dc64551d501fa307289460705f6fccd84cbfc7926d10')
    version('0.19.1', sha256='a19a2ca7a7336495ec180adeaa0dfdcf41e96dbbee90d51c3ed828ba570884e6')
    version('0.18.1', sha256='8ab6e9c808bf2fb3e8576cd8cf07226d9cdc18b012c06d9708429a821ac6634e')
    version('0.17.0', sha256='f600b755fb69437d0f70361f9e560ab4d304b1b66987ed5a28bdd9dd7793e089')
    version('0.15.1', sha256='a212cbc3b79e9a563aa45fc5c517b3499198bd7eb7e7be1e047568a5f48c259a')
    version('0.15.0', sha256='0c74e31e08acc8bf9b6ceb9bced73df2ae0cc76003e0366350bc7b26292bf8b1')

    depends_on('python@2.6:2.8,3.2:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.18:', type=('build', 'run'))
    depends_on('python@3.5:', when='@1.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pybind11@2.4.0:', when='@1.4.1:', type='build')
    depends_on('py-pybind11@2.2.4:', when='@1.4.0:', type='build')
    depends_on('py-numpy@1.5.1:+blas+lapack', type=('build', 'run'))
    depends_on('py-numpy@1.6.2:+blas+lapack', when='@0.16:', type=('build', 'run'))
    depends_on('py-numpy@1.7.1:+blas+lapack', when='@0.18:', type=('build', 'run'))
    depends_on('py-numpy@1.8.2:+blas+lapack', when='@0.19:', type=('build', 'run'))
    depends_on('py-numpy@1.13.3:+blas+lapack', when='@1.3:', type=('build', 'run'))
    depends_on('py-pytest', type='test')

    # NOTE: scipy picks up Blas/Lapack from numpy, see
    # http://www.scipy.org/scipylib/building/linux.html#step-4-build-numpy-1-5-0
    depends_on('blas')
    depends_on('lapack')

    def setup_build_environment(self, env):
        # https://github.com/scipy/scipy/issues/11611
        if self.spec.satisfies('@:1.4 %gcc@10:'):
            env.set('FFLAGS', '-fallow-argument-mismatch')

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
