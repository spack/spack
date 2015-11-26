from spack import *
import shutil

class PyVirtualenv(Package):
    """virtualenv is a tool to create isolated Python environments."""
    homepage = "http://virtualenv.readthedocs.org/projects/virtualenv/"
    url      = "https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz"

    version('1.11.6', 'f61cdd983d2c4e6aeabb70b1060d6f49')
    version('13.0.1', '1ffc011bde6667f0e37ecd976f4934db')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
