from spack import *
import os

class Nccmp(Package):
    """Compare NetCDF Files"""
    homepage = "http://nccmp.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/nccmp/nccmp-1.8.2.0.tar.gz"

    version('1.8.2.0', '81e6286d4413825aec4327e61a28a580')

    depends_on('netcdf')

    def install(self, spec, prefix):
        # Configure says: F90 and F90FLAGS are replaced by FC and
        # FCFLAGS respectively in this configure, please unset
        # F90/F90FLAGS and set FC/FCFLAGS instead and rerun configure
        # again.
        os.environ['FC'] = os.environ['F90']
        del os.environ['F90']
        try:
            os.environ['FCFLAGS'] = os.environ['F90FLAGS']
            del os.environ['F90FLAGS']
        except KeyError:    # There are no flags
            pass

        configure('--prefix=%s' % prefix)

        make()
        make("check")
        make("install")
