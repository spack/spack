from spack import *

class PyStorm(Package):
    """Storm is an object-relational mapper (ORM) for Python"""
    homepage = "https://storm.canonical.com/"
    url      = "https://launchpad.net/storm/trunk/0.20/+download/storm-0.20.tar.gz"

    version('0.20', '8628503141f0f06c0749d607ac09b9c7')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

