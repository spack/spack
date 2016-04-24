from spack import *

class PyOpenpyxl(Package):
    """
    A Python library to read/write Excel 2007 xlsx/xlsm files
    """
    homepage = 'http://openpyxl.readthedocs.org/'
    url      = "https://pypi.python.org/packages/source/o/openpyxl/openpyxl-2.4.0-a1.tar.gz"

    version('2.4.0-a1', 'e5ca6d23ceccb15115d45cdf26e736fc')

    extends('python')

    depends_on('py-jdcal')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
