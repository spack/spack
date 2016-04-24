from spack import *

class PyCsvkit(Package):
    """A library of utilities for working with CSV, the king of tabular file
    formats"""

    homepage = 'http://csvkit.rtfd.org/'
    url      = "https://pypi.python.org/packages/source/c/csvkit/csvkit-0.9.1.tar.gz"

    version('0.9.1', '48d78920019d18846933ee969502fff6')

    extends('python')

    depends_on('py-dateutil')
    depends_on('py-dbf')
    depends_on('py-xlrd')
    depends_on('py-SQLAlchemy')
    depends_on('py-six')
    depends_on('py-openpyxl')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
