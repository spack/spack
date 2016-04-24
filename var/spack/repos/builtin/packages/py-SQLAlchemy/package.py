from spack import *

class PySqlalchemy(Package):
    """
    The Python SQL Toolkit and Object Relational Mapper
    """
    homepage = 'http://www.sqlalchemy.org/'
    url      = "https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-1.0.12.tar.gz"

    version('1.0.12', '6d19ef29883bbebdcac6613cf391cac4')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
