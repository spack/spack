from spack import *

class PyPexpect(Package):
    """Pexpect allows easy control of interactive console applications."""
    homepage = "https://pypi.python.org/pypi/pexpect"
    url      = "https://pypi.python.org/packages/source/p/pexpect/pexpect-3.3.tar.gz"

    version('3.3', '0de72541d3f1374b795472fed841dce8')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
