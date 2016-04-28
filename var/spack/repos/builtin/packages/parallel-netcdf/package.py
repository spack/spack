from spack import *

class ParallelNetcdf(Package):
    """Parallel netCDF (PnetCDF) is a library providing high-performance
    parallel I/O while still maintaining file-format compatibility with
    Unidata's NetCDF."""

    homepage = "https://trac.mcs.anl.gov/projects/parallel-netcdf"
    url      = "http://cucis.ece.northwestern.edu/projects/PnetCDF/Release/parallel-netcdf-1.6.1.tar.gz"

    version('1.7.0', '267eab7b6f9dc78c4d0e6def2def3aea4bc7c9f0')
    version('1.6.1', '62a094eb952f9d1e15f07d56e535052604f1ac34')

    depends_on("m4")
    depends_on("mpi")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-mpi=%s" % spec['mpi'].prefix)
        make()
        make("install")
