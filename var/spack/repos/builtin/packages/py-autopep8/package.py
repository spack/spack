from spack import *

class PyAutopep8(Package):
    """Automatic pep8 formatter"""
    homepage = "https://github.com/hhatto/autopep8"
    url      = "https://github.com/hhatto/autopep8/archive/ver1.2.2.tar.gz"

    version('1.2.2', 'def3d023fc9dfd1b7113602e965ad8e1')

    extends('python')
    depends_on('py-setuptools')
    depends_on('py-pep8')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

