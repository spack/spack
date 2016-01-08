from spack import *

class PyPyzmq(Package):
    """official Python binding for the ZeroMQ Messaging Library"""
    homepage = "https://github.com/zeromq/pyzmq"
    url      = "https://pypi.python.org/packages/source/p/pyzmq/pyzmq-14.7.0.tar.gz"

    version('14.4.1','a6a7fb6950b1bf5333c6795f3edf196c',
           url='https://pypi.python.org/packages/source/p/pyzmq/pyzmq-14.4.1.tar.gz')
    version('14.7.0', '87e3abb33af5794db5ae85c667bbf324')

    extends('python')
    depends_on('py-setuptools@18.1')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
