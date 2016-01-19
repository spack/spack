from spack import *

class PyPytz(Package):
    """World timezone definitions, modern and historical."""
    homepage = "https://pypi.python.org/pypi/pytz"
    url      = "https://pypi.python.org/packages/source/p/pytz/pytz-2014.10.tar.gz"

    version('2014.10', 'eb1cb941a20c5b751352c52486aa1dd7')
    version('2015.4', '417a47b1c432d90333e42084a605d3d8')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
