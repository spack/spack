# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install netcdf-cxx4
#
# You can always get back here to change things with:
#
#     spack edit netcdf-cxx4
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class NetcdfCxx4(Package):
    """C++ interface for NetCDF4"""
    homepage = "http://www.unidata.ucar.edu/downloads/netcdf/netcdf-cxx/index.jsp"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx4-4.2.tar.gz"

    version('4.2', 'd019853802092cf686254aaba165fc81')


    variant('mpi', default=True, description='Enables MPI parallelism')
#    variant('hdf4',    default=False, description="Enable HDF4 support")

    # NetCDF-CXX4 doesn't really depend (directly) on MPI.  However... this
    # depndency ensures taht the right version of MPI is selected (eg: ^openmpi)
    depends_on('mpi', when='+mpi')
    depends_on('netcdf')

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
