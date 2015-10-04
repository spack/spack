from spack import *


class PyPy4j(Package):
    """Enables Python programs to dynamically access arbitrary Java objects"""
    homepage = "https://www.py4j.org/"
    url      = "https://pypi.python.org/packages/source/p/py4j/py4j-0.9.tar.gz"

    version('0.9', 'b6fed5faef81a5368e3d50a91a5c9a60')

    extends("python")
    depends_on("py-setuptools@18.1")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
