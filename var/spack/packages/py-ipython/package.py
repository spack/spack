from spack import *

class PyIpython(Package):
    """IPython provides a rich toolkit to help you make the most out of using Python interactively."""
    homepage = "https://pypi.python.org/pypi/ipython"

    version('3.0.0','b3f00f3c0be036fafef3b0b9d663f27e',
           url='https://pypi.python.org/packages/source/i/ipython/ipython-3.0.0.tar.gz')
    version('4.0.0','c2fecbcf1c0fbdc82625c77a50733dd6',
           url='https://pypi.python.org/packages/source/i/ipython/ipython-4.0.0.tar.gz')
    version('2.3.1', '2b7085525dac11190bfb45bb8ec8dcbf',
            url="https://pypi.python.org/packages/source/i/ipython/ipython-2.3.1.tar.gz")
    version('3.1.0', 'a749d90c16068687b0ec45a27e72ef8f')
    version('3.2.1', 'f4c93d67ac4b2d4fc69df693b6f3c9e0',
            url='https://github.com/ipython/ipython/archive/rel-3.2.1.tar.gz')

    extends('python')
    depends_on('py-pygments')
    depends_on('py-setuptools@18.1')
    depends_on('py-traitlets')
    depends_on('py-pyzmq')
    depends_on('py-pexpect')
    depends_on('py-tornado')
    depends_on('py-jinja2')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
