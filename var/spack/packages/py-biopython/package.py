from spack import *

class PyBiopython(Package):
    """It is a distributed collaborative effort to develop Python libraries and applications which address the needs of current and future work in bioinformatics."""
    homepage = "http://biopython.org/wiki/Main_Page"
    url      = "http://biopython.org/DIST/biopython-1.65.tar.gz"

    version('1.65', '143e7861ade85c0a8b5e2bbdd1da1f67')

    extends('python')
    depends_on('py-mx')
    depends_on('py-numpy')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
