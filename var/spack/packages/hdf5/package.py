from spack import *

class Hdf5(Package):
    """HDF5 is a data model, library, and file format for storing and managing
       data. It supports an unlimited variety of datatypes, and is designed for
       flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "http://www.hdfgroup.org/HDF5/"
    url      = "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.13/src/hdf5-1.8.13.tar.gz"
    list_url = "http://www.hdfgroup.org/ftp/HDF5/releases"
    list_depth = 3

    version('1.8.13', 'c03426e9e77d7766944654280b467289')

    # global variants (eventually need to be handled across all packages)
    variant('debug', default=False, description="Enable debugging")
    variant('static', default=False, description="Build only static libs.")
    variant('fortran', default=True, description="Enable Fortran interfaces.")

    # package specific variants
    variant('cxx', default=True, description="Enable C++ interfaces.")
    variant('mpiio', default=False, description="Enable MPI-IO support.")
    # zlib should be on by default but that currently causes a key error
#    variant('zlib', default=True, description="Enable zlib compression features.")
    variant('zlib', default=False, description="Enable zlib compression features.")

#    depends_on('mpi')
    depends_on('zlib', when='+zlib')
#    depends_on('zlib')

    def install(self, spec, prefix):
        config_args = [
            "CC=cc",
            "CXX=c++",
            "--prefix=%s" % prefix
        ]

        if '+zlib' in spec:
            config_args += ["--with-zlib=%s" % spec['zlib'].prefix]

        if '+debug' in spec:
            config_args += ["--enable-debug=all", "--enable-trace"]
        else:
            config_args += ["--enable-production"]

        if '+static' in spec:
            config_args += ["--disable-shared", "--enable-static"]
        else:
            config_args += ["--enable-shared", "--enable-static"]

        # Note: use ~variant not -variant to test for negated variant in spec
        if '+mpiio' in spec:
            config_args += ["--enable-parallel"]
        elif self.compiler.cc.startswith("mpi") and '~mpiio' not in spec:
            config_args += ["--enable-parallel"]

        # Enable fortran interface if we have a fortran compiler and
        # fortran API isn't explicitly disabled
        if self.compiler.fc and '~fortran' not in spec:
            config_args += ["--enable-fortran", "--enable-fortran2003"]

        # Enable C++ interface if we have a C++ compiler and
        # C++ API isn't explicitly disabled
        if self.compiler.cxx and '~cxx' not in spec:
            config_args += ["--enable-cxx"]

        configure(*config_args)

        make("install")

    def url_for_version(self, version):
        v = str(version)

        if version == Version("1.2.2"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + ".tar.gz"
        elif version < Version("1.7"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + version.up_to(2) + "/hdf5-" + v + ".tar.gz"
        else:
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + "/src/hdf5-" + v + ".tar.gz"
