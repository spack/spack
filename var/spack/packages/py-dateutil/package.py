from spack import *

class PyDateutil(Package):
    """Extensions to the standard Python datetime module."""
    homepage = "https://pypi.python.org/pypi/dateutil"
    url      = "https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.4.0.tar.gz"

    version('2.4.0', '75714163bb96bedd07685cdb2071b8bc')
    version('2.4.2', '4ef68e1c485b09e9f034e10473e5add2')

    extends('python')
    depends_on('py-setuptools')
    depends_on('py-six')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
