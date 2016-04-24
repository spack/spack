from spack import *

class PyXlrd(Package):
    """
    Library for developers to extract data from Microsoft Excel (tm)
    spreadsheet files
    """
    homepage = 'http://www.python-excel.org/'
    url      = "https://pypi.python.org/packages/source/x/xlrd/xlrd-0.9.4.tar.gz"

    version('0.9.4', '911839f534d29fe04525ef8cd88fe865')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
