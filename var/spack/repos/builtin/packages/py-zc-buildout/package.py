from spack import *


class PyZcBuildout(PythonPackage):
    """System for managing development buildouts"""

    homepage = "http://buildout.org/"
    url      = "https://pypi.io/packages/source/z/zc.buildout/zc.buildout-2.13.1.tar.gz"

    version('2.13.1', sha256='3d14d07226963a517295dfad5879d2799e2e3b65b2c61c71b53cb80f5ab11484')

    depends_on('py-setuptools', type='build')
