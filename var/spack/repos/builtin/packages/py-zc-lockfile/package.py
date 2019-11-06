from spack import *


class PyZcLockfile(PythonPackage):
    """Basic inter-process locks """

    homepage = "http://www.python.org/pypi/zc.lockfile"
    url      = "https://pypi.io/packages/source/z/zc.lockfile/zc.lockfile-1.4.tar.gz"

    version(
        '1.4', sha256='95a8e3846937ab2991b61703d6e0251d5abb9604e18412e2714e1b90db173253')

    depends_on('py-setuptools', type=('build', 'run'))
