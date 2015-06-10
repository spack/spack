from spack import *

class PyCffi(Package):
    """Foreign Function Interface for Python calling C code"""
    homepage = "http://cffi.readthedocs.org/en/latest/"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://pypi.python.org/packages/source/c/cffi/cffi-1.1.2.tar.gz#md5="

    version('1.1.2', 'ca6e6c45b45caa87aee9adc7c796eaea')

    extends('python')
    depends_on('py-setuptools')
    depends_on('py-pycparser')
    depends_on('libffi')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
