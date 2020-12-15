# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform


class PyScipy(PythonPackage):
    """SciPy (pronounced "Sigh Pie") is a Scientific Library for Python.
    It provides many user-friendly and efficient numerical routines such
    as routines for numerical integration and optimization."""

    homepage = "https://www.scipy.org/"
    pypi = "scipy/scipy-1.5.4.tar.gz"
    git = "https://github.com/scipy/scipy.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('1.6.3',  sha256='a75b014d3294fce26852a9d04ea27b5671d86736beb34acdfc05859246260707')
    version('1.6.2',  sha256='e9da33e21c9bc1b92c20b5328adb13e5f193b924c9b969cd700c8908f315aa59')
    version('1.6.1',  sha256='c4fceb864890b6168e79b0e714c585dbe2fd4222768ee90bc1aa0f8218691b11')
    version('1.6.0',  sha256='cb6dc9f82dfd95f6b9032a8d7ea70efeeb15d5b5fd6ed4e8537bb3c673580566')
    version('1.5.4',  sha256='4a453d5e5689de62e5d38edf40af3f17560bfd63c9c5bd228c18c1f99afa155b')
    version('1.5.3',  sha256='ddae76784574cc4c172f3d5edd7308be16078dd3b977e8746860c76c195fa707')
    version('1.5.2',  sha256='066c513d90eb3fd7567a9e150828d39111ebd88d3e924cdfc9f8ce19ab6f90c9')
    version('1.5.1',  sha256='039572f0ca9578a466683558c5bf1e65d442860ec6e13307d528749cfe6d07b8')
    version('1.5.0',  sha256='4ff72877d19b295ee7f7727615ea8238f2d59159df0bdd98f91754be4a2767f0')
    version('1.4.1',  sha256='dee1bbf3a6c8f73b6b218cb28eed8dd13347ea2f87d572ce19b289d6fd3fbc59')
    version('1.4.0',  sha256='31f7cfa93b01507c935c12b535e24812594002a02a56803d7cd063e9920d25e8')
    version('1.3.3',  sha256='64bf4e8ae0db2d42b58477817f648d81e77f0b381d0ea4427385bba3f959380a')
    version('1.3.2',  sha256='a03939b431994289f39373c57bbe452974a7da724ae7f9620a1beee575434da4')
    version('1.3.1',  sha256='2643cfb46d97b7797d1dbdb6f3c23fe3402904e3c90e6facfe6a9b98d808c1b5')
    version('1.3.0', sha256='6c1896c3e2738e940f8be132eb7caef48d85f1dc')
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

    depends_on('python@2.6:2.8,3.2:', when='@:0.17.999', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.18:1.2.999', type=('build', 'link', 'run'))
    depends_on('python@3.5:', when='@1.3:1.4.999', type=('build', 'link', 'run'))
    depends_on('python@3.6:', when='@1.5:1.5.999', type=('build', 'link', 'run'))
    depends_on('python@3.7:', when='@1.6:1.6.1', type=('build', 'link', 'run'))
    depends_on('python@3.7:3.9.999', when='@1.6.2:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', when='@:1.6.1', type='build')
    depends_on('py-setuptools@:51.0.0', when='@1.6.2:', type='build')
    depends_on('py-pybind11@2.2.4:', when='@1.4.0', type=('build', 'link'))
    depends_on('py-pybind11@2.4.0:', when='@1.4.1:1.4.999', type=('build', 'link'))
    depends_on('py-pybind11@2.4.3:', when='@1.5:1.6.1', type=('build', 'link'))
    depends_on('py-pybind11@2.4.3:2.6.999', when='@1.6.2:', type=('build', 'link'))
    depends_on('py-numpy@1.5.1:+blas+lapack', when='@:0.15.999', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.6.2:+blas+lapack', when='@0.16:0.17.999', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.7.1:+blas+lapack', when='@0.18:0.18.999', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.8.2:+blas+lapack', when='@0.19:1.2.999', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.13.3:+blas+lapack', when='@1.3:1.4.999', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.14.5:+blas+lapack', when='@1.5:1.5.999', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.16.5:+blas+lapack', when='@1.6:1.6.1', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.16.5:1.22.999+blas+lapack', when='@1.6.2:', type=('build', 'link', 'run'))
    depends_on('py-pytest', type='test')

    # NOTE: scipy picks up Blas/Lapack from numpy, see
    # http://www.scipy.org/scipylib/building/linux.html#step-4-build-numpy-1-5-0
    depends_on('blas')
    depends_on('lapack')

    # https://github.com/scipy/scipy/issues/12860
    patch('https://git.sagemath.org/sage.git/plain/build/pkgs/scipy/patches/extern_decls.patch?id=711fe05025795e44b84233e065d240859ccae5bd',
          sha256='5433f60831cb554101520a8f8871ac5a32c95f7a971ccd68b69049535b106780', when='@1.2:1.5.3')

    def setup_build_environment(self, env):
        # https://github.com/scipy/scipy/issues/9080
        env.set('F90', spack_fc)

        # https://github.com/scipy/scipy/issues/11611
        if self.spec.satisfies('@:1.4 %gcc@10:'):
            env.set('FFLAGS', '-fallow-argument-mismatch')

        # Kluge to get the gfortran linker to work correctly on Big
        # Sur, at least until a gcc release > 10.2 is out with a fix.
        # (There is a fix in their development tree.)
        if platform.mac_ver()[0][0:2] == '11':
            env.set('MACOSX_DEPLOYMENT_TARGET', '10.15')

    def build_args(self, spec, prefix):
        args = []
        if spec.satisfies('%fj'):
            args.extend(['config_fc', '--fcompiler=fujitsu'])

        # Build in parallel
        # Known problems with Python 3.5+
        # https://github.com/spack/spack/issues/7927
        # https://github.com/scipy/scipy/issues/7112
        if not spec.satisfies('^python@3.5:'):
            args.extend(['-j', str(make_jobs)])

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('spack-test', create=True):
            python('-c', 'import scipy; scipy.test("full", verbose=2)')
