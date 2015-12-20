# FIXME: Add copyright

from spack import *
from contextlib import closing
import os

class Otf2(Package):
    """The Open Trace Format 2 is a highly scalable, memory efficient event
       trace data format plus support library."""

    homepage = "http://www.vi-hps.org/score-p"
    url      = "http://www.vi-hps.org/upload/packages/otf2/otf2-1.4.tar.gz"

    version('2.0', '5b546188b25bc1c4e285e06dddf75dfc',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-2.0.tar.gz")
    version('1.5.1', '16a9df46e0da78e374f5d12c8cdc1109',
            url='http://www.vi-hps.org/upload/packages/otf2/otf2-1.5.1.tar.gz')
    version('1.4',   'a23c42e936eb9209c4e08b61c3cf5092',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-1.4.tar.gz")
    version('1.3.1', 'd0ffc4e858455ace4f596f910e68c9f2',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-1.3.1.tar.gz")
    version('1.2.1', '8fb3e11fb7489896596ae2c7c83d7fc8',
            url="http://www.vi-hps.org/upload/packages/otf2/otf2-1.2.1.tar.gz")

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
MPICC=cc
MPICXX=c++
MPIF77=f77
MPIFC=f90
MPI_CFLAGS=-fPIC
MPI_CXXFLAGS=-fPIC
"""

    @when('@:1.2.1')
    def version_specific_args(self):
        return ["--with-platform=disabled", "CC=cc", "CXX=c++", "F77=f77", "F90=f90", "CFLAGS=-fPIC", "CXXFLAGS=-fPIC"]

    @when('@1.3:')
    def version_specific_args(self):
        # TODO: figure out what scorep's build does as of otf2 1.3
        return ["--with-custom-compilers"]

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

        configure_args=["--prefix=%s" % prefix,
                        "--enable-shared"]

        configure_args.extend(self.version_specific_args())

        configure(*configure_args)

        make()
        make("install")
