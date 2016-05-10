from spack import *

class PyPrettytable(Package):
    """
    PrettyTable is a simple Python library designed to make
    it quick and easy to represent tabular data in visually 
    appealing ASCII tables
    """
    homepage = "https://code.google.com/archive/p/prettytable/"
    url      = "https://pypi.python.org/packages/e0/a1/36203205f77ccf98f3c6cf17cf068c972e6458d7e58509ca66da949ca347/prettytable-0.7.2.tar.gz"

    version('0.7.2', 'a6b80afeef286ce66733d54a0296b13b')

    extends("python")
    depends_on("py-setuptools")
    
    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
