from spack import *

class Scons(Package):
    """SCons is a software construction tool"""
    homepage = "http://scons.org"
    url      = "http://downloads.sourceforge.net/project/scons/scons/2.5.0/scons-2.5.0.tar.gz"

    version('2.5.0', '9e00fa0df8f5ca5c5f5975b40e0ed354')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
