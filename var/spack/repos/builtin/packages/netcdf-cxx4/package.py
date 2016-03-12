from spack import *

class NetcdfCxx4(Package):
    """C++ interface for NetCDF4"""
    homepage = "http://www.unidata.ucar.edu/downloads/netcdf/netcdf-cxx/index.jsp"
#    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx4-4.2.tar.gz"
    url      = "https://www.github.com/unidata/netcdf-cxx4/tarball/v123"

#    version('ecdf914', 'afca0c0aeb5c0863c5153c08ad0af534')
    version('ecdf914', git='https://github.com/Unidata/netcdf-cxx4.git', commit='ecdf914')
    version('4.2.1', 'd019853802092cf686254aaba165fc81')


    variant('mpi', default=True, description='Enables MPI parallelism')
#    variant('hdf4',    default=False, description="Enable HDF4 support")

    # NetCDF-CXX4 doesn't really depend (directly) on MPI.  However... this
    # depndency ensures taht the right version of MPI is selected (eg: ^openmpi)
    depends_on('mpi', when='+mpi')
    depends_on('netcdf')

    # Build dependency
    depends_on('cmake')

    def install(self, spec, prefix):
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        with working_dir(build_directory, create=True):
            cmake(source_directory, *std_cmake_args)
            make()
            make("install")
