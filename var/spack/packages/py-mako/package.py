from spack import *

class PyMako(Package):
    """A super-fast templating language that borrows the best 
    ideas from the existing templating languages."""

    homepage = "https://pypi.python.org/pypi/mako"
    url      = "https://pypi.python.org/packages/source/M/Mako/Mako-1.0.1.tar.gz"

    version('1.0.1', '9f0aafd177b039ef67b90ea350497a54')

    depends_on('py-setuptools')
    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
