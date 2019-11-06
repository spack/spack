from spack import *


class PyPortend(PythonPackage):
    """TCP port monitoring and discovery """

    homepage = "https://github.com/jaraco/portend"
    url      = "https://pypi.io/packages/source/p/portend/portend-2.5.tar.gz"

    version(
        '2.5', sha256='19dc27bfb3c72471bd30a235a4d5fbefef8a7e31cab367744b5d87a205e7bfd9')

    depends_on('py-setuptools', type='build')
    depends_on('portend', type=('run','build'))
