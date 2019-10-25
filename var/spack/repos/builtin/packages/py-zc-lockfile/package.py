from spack import *


class PyZcLockfile(PythonPackage):
    """Basic inter-process locks """

    homepage = "http://www.python.org/pypi/zc.lockfile"
    url      = "https://files.pythonhosted.org/packages/58/c2/d7c89bdad237b4b7837609172be3e8bf5630796c0020494a15b97ece8eb1/zc.lockfile-1.4.tar.gz"

    version('1.4', sha256='95a8e3846937ab2991b61703d6e0251d5abb9604e18412e2714e1b90db173253')

    depends_on('py-setuptools', type='build')
