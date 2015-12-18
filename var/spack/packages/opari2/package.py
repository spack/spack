# FIXME: Add copyright statement here 

from spack import *
from contextlib import closing

class Opari2(Package):
    """OPARI2 is a source-to-source instrumentation tool for OpenMP and 
       hybrid codes. It surrounds OpenMP directives and runtime library 
       calls with calls to the POMP2 measurement interface.
       OPARI2 will provide you with a new initialization method that allows 
       for multi-directory and parallel builds as well as the usage of 
       pre-instrumented libraries. Furthermore, an efficient way of 
       tracking parent-child relationships was added. Additionally, we 
       extended OPARI2 to support instrumentation of OpenMP 3.0 
       tied tasks. """

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "http://www.vi-hps.org/upload/packages/opari2/opari2-1.1.2.tar.gz"

    version('1.1.4', '245d3d11147a06de77909b0805f530c0',
            url='http://www.vi-hps.org/upload/packages/opari2/opari2-1.1.4.tar.gz')
    version('1.1.2', '9a262c7ca05ff0ab5f7775ae96f3539e')

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
        # Use a custom compiler configuration, otherwise the score-p
        # build system messes with spack's compiler settings.
        # Create these three files in the build directory
        with closing(open("platform-backend-user-provided", "w")) as backend_file:
            backend_file.write(self.backend_user_provided)
        with closing(open("platform-frontend-user-provided", "w")) as frontend_file:
            frontend_file.write(self.frontend_user_provided)
        with closing(open("platform-mpi-user-provided", "w")) as mpi_file:
            mpi_file.write(self.mpi_user_provided)            

        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix,
                  "--with-custom-compilers",
                  "--enable-shared")

        # FIXME: Add logic to build and install here
        make()
        make("install")
