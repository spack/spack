from spack import *
import re

class PyH5py(Package):
    """The h5py package provides both a high- and low-level interface to the HDF5 library from Python."""
    homepage = "https://pypi.python.org/pypi/h5py"
    url      = "https://pypi.python.org/packages/source/h/h5py/h5py-2.4.0.tar.gz"

    version('2.4.0', '80c9a94ae31f84885cc2ebe1323d6758')
    version('2.5.0', '6e4301b5ad5da0d51b0a1e5ac19e3b74')

    extends('python', ignore=lambda f: re.match(r'bin/cy*', f))
    depends_on('hdf5')
    depends_on('py-numpy')
    depends_on('py-cython')

    def install(self, spec, prefix):
        python('setup.py', 'configure', '--hdf5=%s' % spec['hdf5'].prefix)
        python('setup.py', 'install', '--prefix=%s' % prefix)
