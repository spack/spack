from spack import *

class Hdf(Package):
    """HDF4 (also known as HDF) is a library and multi-object
    file format for storing and managing data between machines."""

    homepage = "https://www.hdfgroup.org/products/hdf4/"
    url      = "https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.11/src/hdf-4.2.11.tar.gz"
    list_url = "https://www.hdfgroup.org/ftp/HDF/releases/"
    list_depth = 3

    version('4.2.11', '063f9928f3a19cc21367b71c3b8bbf19')

    variant('szip', default=False, description="Enable szip support")

    depends_on("jpeg")
    depends_on("szip", when='+szip')
    depends_on("zlib")


    def url_for_version(self, version):
       return "https://www.hdfgroup.org/ftp/HDF/releases/HDF" + str(version) + "/src/hdf-" + str(version) + ".tar.gz"


    def install(self, spec, prefix):
        config_args = [
            'CFLAGS=-fPIC',
            '--prefix=%s' % prefix,
            '--with-jpeg=%s' % spec['jpeg'].prefix,
            '--with-zlib=%s' % spec['zlib'].prefix,
            '--disable-netcdf',  # must be disabled to build NetCDF with HDF4 support
            '--enable-fortran',
            '--disable-shared',  # fortran and shared libraries are not compatible
            '--enable-static',
            '--enable-production'
        ]

        # SZip support
        if '+szip' in spec:
            config_args.append('--with-szlib=%s' % spec['szip'].prefix)

        configure(*config_args)

        make()
        make("install")
