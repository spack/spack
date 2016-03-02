from spack import *

class NetcdfCxx4(Package):
    """C++ interface for NetCDF4"""
    homepage = "http://www.unidata.ucar.edu/downloads/netcdf/netcdf-cxx/index.jsp"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx4-4.2.tar.gz"

    version('4.2', 'd019853802092cf686254aaba165fc81')


    variant('mpi', default=True, description='Enables MPI parallelism')

    # netcdf-cxx4 doesn't really depend (directly) on MPI.  However... this
    # depndency ensures taht the right version of MPI is selected (eg: ^openmpi)
    depends_on('mpi', when='+mpi')
    depends_on('netcdf')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
