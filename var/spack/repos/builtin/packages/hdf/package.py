from spack import *

class Hdf(Package):
    """HDF4 (also known as HDF) is a library and multi-object
    file format for storing and managing data between machines."""

    homepage = "https://www.hdfgroup.org/products/hdf4/"
    url      = "https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.11/src/hdf-4.2.11.tar.gz"
    list_url = "https://www.hdfgroup.org/ftp/HDF/releases/"
    list_depth = 3

    version('4.2.11', '063f9928f3a19cc21367b71c3b8bbf19')

    depends_on("jpeg")
    depends_on("szip@2.1")
    depends_on("zlib")


    def url_for_version(self, version):
       return "https://www.hdfgroup.org/ftp/HDF/releases/HDF" + str(version) + "/src/hdf-" + str(version) + ".tar.gz"


    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-jpeg=%s'  % spec['jpeg'].prefix,
                  '--with-szlib=%s' % spec['szip'].prefix,
                  '--with-zlib=%s'  % spec['zlib'].prefix,
                  '--disable-netcdf',
                  '--enable-fortran',
                  '--disable-shared',
                  '--enable-static',
                  '--enable-production')

        make()
        make("install")
