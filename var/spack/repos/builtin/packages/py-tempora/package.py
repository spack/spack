from spack import *


class PyTempora(PythonPackage):
    """Objects and routines pertaining to date and time (tempora) """

    homepage = "https://github.com/jaraco/tempora"
    url      = "https://pypi.io/packages/source/t/tempora/tempora-1.14.1.tar.gz"

    version('1.14.1', sha256='cb60b1d2b1664104e307f8e5269d7f4acdb077c82e35cd57246ae14a3427d2d6')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-jaraco-functools@1.20:', type=('build', 'run'))
    depends_on('python@2.7', type=('build', 'run'))
