from spack import *

class PyPyelftools(Package):
    """A pure-Python library for parsing and analyzing ELF files and DWARF debugging information"""
    homepage = "https://pypi.python.org/pypi/pyelftools"
    url      = "https://pypi.python.org/packages/source/p/pyelftools/pyelftools-0.23.tar.gz"

    version('0.23', 'aa7cefa8bd2f63d7b017440c9084f310')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
