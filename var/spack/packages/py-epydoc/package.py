from spack import *

class PyEpydoc(Package):
    """Epydoc is a tool for generating API documentation documentation for Python modules, based on their docstrings."""
    homepage = "https://pypi.python.org/pypi/epydoc"
    url      = "https://pypi.python.org/packages/source/e/epydoc/epydoc-3.0.1.tar.gz"

    version('3.0.1', '36407974bd5da2af00bf90ca27feeb44')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
