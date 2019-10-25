from spack import *


class PyTempora(PythonPackage):
    """Objects and routines pertaining to date and time (tempora) """

    homepage = "https://github.com/jaraco/tempora"
    url      = "https://files.pythonhosted.org/packages/2f/b5/5b0464385454c5ca93a39a1c6acefdf574aeb10ef45fa8958b3832cc7d96/tempora-1.14.1.tar.gz"

    version('1.14.1', sha256='cb60b1d2b1664104e307f8e5269d7f4acdb077c82e35cd57246ae14a3427d2d6')

    depends_on('py-setuptools', type='build')
    depends_on('py-jaraco-functools', type='build')
