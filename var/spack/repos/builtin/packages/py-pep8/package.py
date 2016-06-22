from spack import *

class PyPep8(Package):
    """python pep8 format checker"""
    homepage = "https://github.com/PyCQA/pycodestyle"
    url      = "https://github.com/PyCQA/pycodestyle/archive/1.7.0.tar.gz"

    version('1.7.0', '31070a3a6391928893cbf5fa523eb8d9')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

