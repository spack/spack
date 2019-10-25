
from spack import *


class PyCheroot(PythonPackage):
    """ Highly-optimized, pure-python HTTP server """

    homepage = "https://cheroot.cherrypy.org/"
    url      = "https://files.pythonhosted.org/packages/0c/d9/4e13bc35e920ec63fc0f6b01f84537e9a7b9d6462a0419d903fea591a723/cheroot-6.5.5.tar.gz"

    version('6.5.5', sha256='f6a85e005adb5bc5f3a92b998ff0e48795d4d98a0fbb7edde47a7513d4100601')

    depends_on('py-setuptools', type='build')
