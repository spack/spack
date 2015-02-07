from spack import *
import shutil

class PyVirtualenv(Package):
    """virtualenv is a tool to create isolated Python environments."""
    homepage = "http://virtualenv.readthedocs.org/projects/virtualenv/"
    url      = "https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz"

    version('1.11.6', 'f61cdd983d2c4e6aeabb70b1060d6f49')

    extends('python')

    def clean(self):
        if os.path.exists('build'):
            shutil.rmtree('build')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
