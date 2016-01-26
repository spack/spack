from spack import *

class PyUrwid(Package):
    """A full-featured console UI library"""
    homepage = "http://urwid.org/"
    url      = "https://pypi.python.org/packages/source/u/urwid/urwid-1.3.0.tar.gz"

    version('1.3.0', 'a989acd54f4ff1a554add464803a9175')

    depends_on('py-setuptools')

    extends("python")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

