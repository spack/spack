from spack import *

class PyGnuplot(Package):
    """Gnuplot.py is a Python package that allows you to create graphs from within Python using the gnuplot plotting program."""
    homepage = "http://gnuplot-py.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/gnuplot-py/Gnuplot-py/1.8/gnuplot-py-1.8.tar.gz"

    version('1.8', 'abd6f571e7aec68ae7db90a5217cd5b1')

    extends('python')
    depends_on('py-numpy')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
