from spack import *

class PyYapf(Package):
    """ Yet Another Python Formatter """
    homepage = "https://github.com/google/yapf"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://github.com/google/yapf/archive/v0.2.1.tar.gz"

    version('0.2.1', '348ccf86cf2057872e4451b204fb914c')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
