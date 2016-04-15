from spack import *

class ParallelNetcdf(Package):
    """Parallel netCDF (PnetCDF) is a library providing high-performance
    parallel I/O while still maintaining file-format compatibility with
    Unidata's NetCDF."""

    homepage = "https://trac.mcs.anl.gov/projects/parallel-netcdf"
    url      = "http://cucis.ece.northwestern.edu/projects/PnetCDF/Release/parallel-netcdf-1.6.1.tar.gz"

    version('1.6.1', '62a094eb952f9d1e15f07d56e535052604f1ac34')

    variant('cxx', default=True, description='Build the C++ Interface')
    variant('fortran', default=True, description='Build the Fortran Interface')
    variant('fpic', default=True, description='Produce position-independent code (for use with shared libraries)')

    depends_on("m4")
    depends_on("mpi")

    # See: https://trac.mcs.anl.gov/projects/parallel-netcdf/browser/trunk/INSTALL
    def install(self, spec, prefix):
        args = list()
        if '+fpic' in spec:
            args.extend(['CFLAGS=-fPIC', 'CXXFLAGS=-fPIC', 'FFLAGS=-fPIC'])
        if '~cxx' in spec:
            args.append('--disable-cxx')
        if '~fortran' in spec:
            args.append('--disable-fortran')

        args.extend(["--prefix=%s" % prefix,
                  "--with-mpi=%s" % spec['mpi'].prefix])
        configure(*args)
        make()
        make("install")
