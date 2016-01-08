from spack import *

class PyTraitlets(Package):
    """A lightweight Traits like module"""
    homepage = "http://traitlets.readthedocs.org/"
    url      = "https://github.com/ipython/traitlets/archive/4.0.0.tar.gz"

    version('4.0.0', 'b5b95ea5941fd9619b4704dfd8201568')

    extends('python')
    depends_on("py-setuptools@18.1")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
