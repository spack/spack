from spack import *

class PyScientificpython(Package):
    """ScientificPython is a collection of Python modules for
       scientific computing. It contains support for geometry,
       mathematical functions, statistics, physical units, IO,
       visualization, and parallelization."""

    homepage = "https://sourcesup.renater.fr/projects/scientific-py/"
    url      = "https://sourcesup.renater.fr/frs/download.php/file/4411/ScientificPython-2.8.1.tar.gz"
    version('2.8.1', '73ee0df19c7b58cdf2954261f0763c77')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
