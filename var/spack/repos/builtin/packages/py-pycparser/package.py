from spack import *

class PyPycparser(Package):
    """pycparser is a complete parser of the C language, written in pure python"""
    homepage = "https://github.com/eliben/pycparser"
    url      = "https://pypi.python.org/packages/source/p/pycparser/pycparser-2.13.tar.gz"

    version('2.13', 'e4fe1a2d341b22e25da0d22f034ef32f')

    
    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
