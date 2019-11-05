from spack import *


class PyJaracoFunctools(PythonPackage):
    """Functools like those found in stdlib"""

    homepage = "https://github.com/jaraco/jaraco.functools"
    url      = "https://files.pythonhosted.org/packages/a9/1e/44f6a5cffef147a3ffd37a748b8f4c2ded9b07ca20a15f17cd9874158f24/jaraco.functools-2.0.tar.gz"

    version(
        '2.0', sha256='35ba944f52b1a7beee8843a5aa6752d1d5b79893eeb7770ea98be6b637bf9345')

    depends_on('py-setuptools', type='build')
