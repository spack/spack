from spack import *

class PyMysqldb1(Package):
    """Legacy mysql bindings for python"""
    homepage = "https://github.com/farcepest/MySQLdb1"
    url      = "https://github.com/farcepest/MySQLdb1/archive/MySQLdb-1.2.5.tar.gz"

    version('1.2.5', '332c8f4955b6bc0c79ea15170bf7321b')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

