from spack import *

class PyScipy(Package):
    """Scientific Library for Python."""
    homepage = "https://pypi.python.org/pypi/scipy"
    url      = "https://pypi.python.org/packages/source/s/scipy/scipy-0.15.0.tar.gz"

    version('0.15.0', '639112f077f0aeb6d80718dc5019dc7a')

    extends('python')
    depends_on('py-nose')
    depends_on('py-numpy')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
