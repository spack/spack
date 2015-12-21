# FIXME: Add copyright statement
#
from spack import *
from contextlib import closing

class Cube(Package):
    """Cube the profile viewer for Score-P and Scalasca profiles. It 
       displays a multi-dimensional performance space consisting 
       of the dimensions (i) performance metric, (ii) call path, 
       and (iii) system resource."""

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url      = "http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-4.2.3.tar.gz"

    version('4.3.3', '07e109248ed8ffc7bdcce614264a2909',
            url='http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3.3.tar.gz')

    version('4.2.3', '8f95b9531f5a8f8134f279c2767c9b20')

    version('4.3TP1', 'a2090fbc7b2ba394bd5c09ba971e237f', 
            url = 'http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3-TP1.tar.gz')

    # Using CC as C++ compiler provides quirky workaround for a Score-P build system attempt 
    # to guess a matching C compiler when configuring scorep-score
    backend_user_provided = """\
CC=cc
CXX=CC
F77=f77
FC=f90
#CFLAGS=-fPIC
#CXXFLAGS=-fPIC
"""
    frontend_user_provided = """\
CC_FOR_BUILD=cc
CXX_FOR_BUILD=CC
F77_FOR_BUILD=f70
FC_FOR_BUILD=f90
"""

    def install(self, spec, prefix):
        # Use a custom compiler configuration, otherwise the score-p
        # build system messes with spack's compiler settings.
        # Create these three files in the build directory

        with closing(open("vendor/common/build-config/platforms/platform-backend-user-provided", "w")) as backend_file:
            backend_file.write(self.backend_user_provided)
        with closing(open("vendor/common/build-config/platforms/platform-frontend-user-provided", "w")) as frontend_file:
            frontend_file.write(self.frontend_user_provided)

        configure_args = ["--prefix=%s" % prefix,
                          "--with-custom-compilers",
                          "--without-paraver", 
                          "--without-gui"]

        configure(*configure_args)

        make(parallel=False)
        make("install", parallel=False)
