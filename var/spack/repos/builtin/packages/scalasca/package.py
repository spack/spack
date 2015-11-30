# FIXME: Add copyright

from spack import *

class Scalasca(Package):
    """Scalasca is a software tool that supports the performance optimization
       of parallel programs by measuring and analyzing their runtime behavior. 
       The analysis identifies potential performance bottlenecks - in 
       particular those concerning communication and synchronization - and 
       offers guidance in exploring their causes."""

    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.scalasca.org"
    url      = "http://apps.fz-juelich.de/scalasca/releases/scalasca/2.1/dist/scalasca-2.1.tar.gz"

    version('2.1', 'bab9c2b021e51e2ba187feec442b96e6', 
            url = 'http://apps.fz-juelich.de/scalasca/releases/scalasca/2.1/dist/scalasca-2.1.tar.gz' )

    depends_on("mpi")
    depends_on("otf2@1.4")
    depends_on("cube@4.2.3")

    backend_user_provided = """\
CC=cc
CXX=c++
F77=f77
FC=f90
CFLAGS=-fPIC
CXXFLAGS=-fPIC
"""
    frontend_user_provided = """\
CC_FOR_BUILD=cc
CXX_FOR_BUILD=c++
F77_FOR_BUILD=f70
FC_FOR_BUILD=f90
CFLAGS_FOR_BUILD=-fPIC
CXXFLAGS_FOR_BUILD=-fPIC
"""
    mpi_user_provided = """\
MPICC=mpicc
MPICXX=mpicxx
MPIF77=mpif77
MPIFC=mpif90
MPI_CFLAGS=-fPIC
MPI_CXXFLAGS=-fPIC
"""

    def install(self, spec, prefix):
        configure_args = ["--prefix=%s" % prefix,
                          "--with-custom-compilers", 
                          "--with-otf2=%s" % spec['otf2'].prefix.bin,
                          "--with-cube=%s" % spec['cube'].prefix.bin,
                          "--enable-shared"]

        configure(*configure_args)

        make()
        make("install")

        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
