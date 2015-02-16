from spack import *

class PyLibxml2(Package):
    """A Python wrapper around libxml2."""
    homepage = "https://xmlsoft.org/python.html"
    url      = "ftp://xmlsoft.org/libxml2/python/libxml2-python-2.6.21.tar.gz"

    version('2.6.21', '229dd2b3d110a77defeeaa73af83f7f3')

    extends('python')
    depends_on('libxml2')
    depends_on('libxslt')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
