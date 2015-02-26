from spack import *

class PySetuptools(Package):
    """Easily download, build, install, upgrade, and uninstall Python packages."""
    homepage = "https://pypi.python.org/pypi/setuptools"
    url      = "https://pypi.python.org/packages/source/s/setuptools/setuptools-11.3.tar.gz"

    version('11.3.1', '01f69212e019a2420c1693fb43593930')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
