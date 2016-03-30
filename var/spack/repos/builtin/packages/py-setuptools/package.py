from spack import *

class PySetuptools(Package):
    """Easily download, build, install, upgrade, and uninstall Python packages."""
    homepage = "https://pypi.python.org/pypi/setuptools"
    url      = "https://pypi.python.org/packages/source/s/setuptools/setuptools-11.3.tar.gz"

    version('11.3.1', '01f69212e019a2420c1693fb43593930')
    version('16.0', '0ace0b96233516fc5f7c857d086aa3ad')
    version('18.1', 'f72e87f34fbf07f299f6cb46256a0b06')
    version('19.2', '78353b1f80375ca5e088f4b4627ffe03')
    version('20.5', 'fadc1e1123ddbe31006e5e43e927362b')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
