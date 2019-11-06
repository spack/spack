from spack import *


class PyJaracoFunctools(PythonPackage):
    """Functools like those found in stdlib"""

    homepage = "https://github.com/jaraco/jaraco.functools"
    url      = "https://pypi.io/packages/source/j/jaraco.functools/jaraco.functools-2.0.tar.gz"

    version(
        '2.0', sha256='35ba944f52b1a7beee8843a5aa6752d1d5b79893eeb7770ea98be6b637bf9345')

    depends_on('py-setuptools', type='build')
