from spack import *
import os

class PyPbr(Package):
    """PBR is a library that injects some useful and sensible default behaviors into your setuptools run."""
    homepage = "https://pypi.python.org/pypi/pbr"
    url      = "https://pypi.python.org/packages/source/p/pbr/pbr-1.8.1.tar.gz"

    version('1.8.1', 'c8f9285e1a4ca6f9654c529b158baa3a')

    extends('python')

    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)


