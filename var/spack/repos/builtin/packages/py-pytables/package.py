from spack import *
import re

class PyPytables(Package):
    """PyTables is a package for managing hierarchical datasets and designed to efficiently and easily cope with extremely large amounts of data."""
    homepage = "http://www.pytables.org/"
    url      = "https://github.com/PyTables/PyTables/archive/v.3.2.2.tar.gz"

    version('3.2.2', '7cbb0972e4d6580f629996a5bed92441')

    extends('python')
    depends_on('hdf5')
    depends_on('py-numpy')
    depends_on('py-numexpr')
    depends_on('py-cython')

    def install(self, spec, prefix):
        env["HDF5_DIR"] = spec['hdf5'].prefix
        python('setup.py', 'install', '--prefix=%s' % prefix)
