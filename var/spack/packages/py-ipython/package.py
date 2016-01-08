from spack import *

class PyIpython(Package):
    """IPython provides a rich toolkit to help you make the most out of using Python interactively."""
    homepage = "https://pypi.python.org/pypi/ipython"
    url      = "https://pypi.python.org/packages/source/i/ipython/ipython-2.3.1.tar.gz"

    version('2.3.1', '2b7085525dac11190bfb45bb8ec8dcbf')
    version('3.1.0', 'a749d90c16068687b0ec45a27e72ef8f')

    extends('python')
    depends_on('py-pygments')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
