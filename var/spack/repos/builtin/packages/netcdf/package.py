from spack import *

class Netcdf(Package):
    """NetCDF is a set of software libraries and self-describing, machine-independent
    data formats that support the creation, access, and sharing of array-oriented
    scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf/"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.4.0', 'f01cb26a0126dd9a6224e76472d25f6c')
    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    variant('fortran', default=False, description="Download and install NetCDF-Fortran")
    variant('hdf4', default=False, description="Enable HDF4 support")

    patch('netcdf-4.3.3-mpi.patch')

    # Dependencies:
    depends_on("curl")  # required for DAP support
    depends_on("hdf", when='+hdf4')
    depends_on("hdf5")  # required for NetCDF-4 support
    depends_on("zlib")  # required for NetCDF-4 support

    def install(self, spec, prefix):
        config_args = [
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

        # HDF4 support
        if '+hdf4' in spec:
            config_args.append("--enable-hdf4")

        # Fortran support
        # In version 4.2+, NetCDF-C and NetCDF-Fortran have split.
        # They can be installed separately, but this bootstrap procedure
        # should be able to install both at the same time.
        # Note: this is a new experimental feature
        if '+fortran' in spec:
            config_args.append("--enable-remote-fortran-bootstrap")

        configure(*config_args)
        make()
        make("install")
