from spack import *

class PyMatplotlib(Package):
    """Python plotting package."""
    homepage = "https://pypi.python.org/pypi/matplotlib"
    url      = "https://pypi.python.org/packages/source/m/matplotlib/matplotlib-1.4.2.tar.gz"

    version('1.4.2', '7d22efb6cce475025733c50487bd8898')

    extends('python')
    depends_on('py-pyside')
    depends_on('py-ipython')
    depends_on('py-pyparsing')
    depends_on('py-six')
    depends_on('py-dateutil')
    depends_on('py-pytz')
    depends_on('py-nose')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
