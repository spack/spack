from spack import *

class Muster(Package):
    """The Muster library provides implementations of sequential and
       parallel K-Medoids clustering algorithms. It is intended as a
       general framework for parallel cluster analysis, particularly
       for performance data analysis on systems with very large
       numbers of processes.
    """
    homepage = "https://github.com/scalability-llnl/muster"
    url      = "https://github.com/scalability-llnl/muster/archive/v1.0.tar.gz"

    version('1.0.1', 'd709787db7e080447afb6571ac17723c')
    version('1.0',   '2eec6979a4a36d3a65a792d12969be16')

    depends_on("boost")
    depends_on("mpi")

    def install(self, spec, prefix):
        cmake(".", *std_cmake_args)
        make()
        make("install")
