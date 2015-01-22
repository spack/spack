from spack import *

class PyPil(Package):
    """The Python Imaging Library (PIL) adds image processing capabilities to your Python interpreter. This library supports many file formats, and provides powerful image processing and graphics capabilities."""

    homepage = "http://www.pythonware.com/products/pil/"
    url      = "http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz"

    version('1.1.7', 'fc14a54e1ce02a0225be8854bfba478e')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
