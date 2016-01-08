from spack import *

class PyTornado(Package):
    """Python web framework and asynchronous networking library"""
    homepage = "http://www.tornadoweb.org/"
    url = "https://pypi.python.org/packages/source/t/tornado/tornado-4.2.1.tar.gz"

    version('4.0.2','985c0e704b765c33a6193d49d1935588',
           url='https://pypi.python.org/packages/source/t/tornado/tornado-4.0.2.tar.gz')
    version('4.2.1', 'd523204389cfb70121bb69709f551b20')

    extends('python')
    depends_on('py-certifi')
    depends_on('py-setuptools@18.1')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
