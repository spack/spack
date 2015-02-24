from spack import *
import re

class PyPylint(Package):
    """array processing for numbers, strings, records, and objects."""
    homepage = "https://pypi.python.org/pypi/pylint"
    url      = "https://pypi.python.org/packages/source/p/pylint/pylint-1.4.1.tar.gz"

    version('1.4.1', 'df7c679bdcce5019389038847e4de622')

    extends('python')
    depends_on('py-nose')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
