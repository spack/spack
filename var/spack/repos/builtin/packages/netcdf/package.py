from spack import *


class Netcdf(Package):
    """NetCDF is a set of software libraries and self-describing, machine-independent
    data formats that support the creation, access, and sharing of array-oriented
    scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.4.0', 'cffda0cbd97fdb3a06e9274f7aef438e')
    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    variant('mpi', default=True, description='Enables MPI parallelism')
    variant('hdf4',    default=False, description="Enable HDF4 support")

    # Dependencies:
    depends_on("curl")  # required for DAP support
    depends_on("hdf", when='+hdf4')
    depends_on("hdf5+mpi~cxx", when='+mpi')  # required for NetCDF-4 support
    depends_on("hdf5~mpi", when='~mpi')  # required for NetCDF-4 support
    depends_on("zlib")  # required for NetCDF-4 support

    # ======= From NetCDF release notes:
    # The first release candidate for the netCDF-C library version 4.4.1
    # is now available. There have been a number of improvements since
    # the 4.4.0 release. Most importantly, this release candidate is
    # able to write backwards-compatible netCDF4 files when using HDF5
    # version 1.10.0. As announced previously, using HDF5 1.10.0 with
    # netCDF 4.4.0 would result in netCDF4 files which were unreadable
    # by systems using an earlier version of libhdf5. See GitHub #250
    # for more information.
#    depends_on('hdf5@:1.9', when='@:4.4.0')
#    depends_on('hdf5@1.10:', when='@4.4.1:')


    def install(self, spec, prefix):
        # Environment variables
        CPPFLAGS = []
        LDFLAGS  = []
        LIBS     = []

        config_args = [
            "--prefix=%s" % prefix,
            "--enable-fsync",
            "--enable-v2",
            "--enable-utilities",
            "--enable-shared",
            "--enable-static",
            "--enable-largefile",
            # necessary for HDF5 support
            "--enable-netcdf-4",
            "--enable-dynamic-loading",
            # necessary for DAP support
            "--enable-dap"
        ]

        # Make sure Netcdf links against Spack's curl
        # Otherwise it may pick up system's curl, which could lead to link errors:
        # /usr/lib/x86_64-linux-gnu/libcurl.so: undefined reference to `SSL_CTX_use_certificate_chain_file@OPENSSL_1.0.0'
        LIBS.append("-lcurl")
        CPPFLAGS.append("-I%s" % spec['curl'].prefix.include)
        LDFLAGS.append ("-L%s" % spec['curl'].prefix.lib)

        if '+mpi' in spec:
            config_args.append('--enable-parallel4')

        CPPFLAGS.append("-I%s/include" % spec['hdf5'].prefix)
        LDFLAGS.append( "-L%s/lib"     % spec['hdf5'].prefix)

        # HDF4 support
        # As of NetCDF 4.1.3, "--with-hdf4=..." is no longer a valid option
        # You must use the environment variables CPPFLAGS and LDFLAGS
        if '+hdf4' in spec:
            config_args.append("--enable-hdf4")
            CPPFLAGS.append("-I%s/include" % spec['hdf'].prefix)
            LDFLAGS.append( "-L%s/lib"     % spec['hdf'].prefix)
            LIBS.append(    "-l%s"         % "jpeg")

        if 'szip' in spec:
            CPPFLAGS.append("-I%s/include" % spec['szip'].prefix)
            LDFLAGS.append( "-L%s/lib"     % spec['szip'].prefix)
            LIBS.append(    "-l%s"         % "sz")

        # Fortran support
        # In version 4.2+, NetCDF-C and NetCDF-Fortran have split.
        # Use the netcdf-fortran package to install Fortran support.

        config_args.append('CPPFLAGS=%s' % ' '.join(CPPFLAGS))
        config_args.append('LDFLAGS=%s'  % ' '.join(LDFLAGS))
        config_args.append('LIBS=%s'     % ' '.join(LIBS))

        configure(*config_args)
        make()
        make("install")
