from spack import *

class PyTwisted(Package):
    """An asynchronous networking framework written in Python"""
    homepage = "https://twistedmatrix.com/"
    url      = "https://pypi.python.org/packages/source/T/Twisted/Twisted-15.3.0.tar.bz2"

    version('15.4.0', '5337ffb6aeeff3790981a2cd56db9655')
    version('15.3.0', 'b58e83da2f00b3352afad74d0c5c4599')

    depends_on('py-setuptools')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
