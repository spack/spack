# FIXME: Add copyright statement

from spack import *

class Scorep(Package):
    """The Score-P measurement infrastructure is a highly scalable and
       easy-to-use tool suite for profiling, event tracing, and online
       analysis of HPC applications."""

    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "http://www.vi-hps.org/upload/packages/scorep/scorep-1.2.3.tar.gz"

    version('1.3', '9db6f957b7f51fa01377a9537867a55c',
            url = 'http://www.vi-hps.org/upload/packages/scorep/scorep-1.3.tar.gz')

    version('1.2.3', '4978084e7cbd05b94517aa8beaea0817')

    depends_on("mpi")
    depends_on("papi")
    # depends_on("otf2@1.2:1.2.1") # only Score-P 1.2.x
    depends_on("otf2")
    depends_on("opari2")
    depends_on("cube@4.2:4.2.3")

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
        with open("platform-backend-user-provided", "w") as backend_file:
            backend_file.write(self.backend_user_provided)
        with open("platform-frontend-user-provided", "w") as frontend_file:
            frontend_file.write(self.frontend_user_provided)
        with open("platform-mpi-user-provided", "w") as mpi_file:
            mpi_file.write(self.mpi_user_provided)

        configure_args = ["--prefix=%s" % prefix,
                          "--with-custom-compilers",
                          "--with-otf2=%s" % spec['otf2'].prefix.bin,
                          "--with-opari2=%s" % spec['opari2'].prefix.bin,
                          "--with-cube=%s" % spec['cube'].prefix.bin,
                          "--with-papi-header=%s" % spec['papi'].prefix.include,
                          "--with-papi-lib=%s" % spec['papi'].prefix.lib,
                          "--enable-shared"]

        configure(*configure_args)

        make()
        make("install")
