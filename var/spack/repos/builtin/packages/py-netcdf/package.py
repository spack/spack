from spack import *
import os


class PyNetcdf(Package):
    """Python interface to the netCDF Library."""
    homepage = "http://unidata.github.io/netcdf4-python"
    url      = "https://github.com/Unidata/netcdf4-python/tarball/v1.2.3.1rel"

    version('1.2.3.1', '4fc4320d4f2a77b894ebf8da1c9895af')

    extends('python')
    depends_on('py-numpy')
    depends_on('py-cython')
    depends_on('netcdf')

    def install(self, spec, prefix):

        # Work around lack of RPATH in Python extensions
        py_numpy = self.spec['py-numpy']
        if 'blas' in py_numpy:
            LD_LIBRARY_PATH = [join_path(dep.prefix, 'lib')
                for dep in self.unique_dependencies(py_numpy['blas'])]
            os.environ['LD_LIBRARY_PATH'] = ':'.join(LD_LIBRARY_PATH)

        python('setup.py', 'install', '--prefix=%s' % prefix)
