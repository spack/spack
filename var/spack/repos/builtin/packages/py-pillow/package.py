from spack import *

class PyPillow(Package):
    """Pillow is the friendly PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors. The Python Imaging Library (PIL) adds image processing capabilities to your Python interpreter. This library supports many file formats, and provides powerful image processing and graphics capabilities."""

    homepage = "https://python-pillow.github.io/"
    url      = "https://pypi.python.org/packages/source/P/Pillow/Pillow-3.0.0.tar.gz"

    version('3.0.0', 'fc8ac44e93da09678eac7e30c9b7377d')
    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
