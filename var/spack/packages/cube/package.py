# FIXME: Add copyright statement
#
from spack import *

class Cube(Package):
    """Cube the profile viewer for Score-P and Scalasca profiles. It 
       displays a multi-dimensional performance space consisting 
       of the dimensions (i) performance metric, (ii) call path, 
       and (iii) system resource."""

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url      = "http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-4.2.3.tar.gz"

    version('4.2.3', '8f95b9531f5a8f8134f279c2767c9b20')

    def install(self, spec, prefix):
        configure_args = ["--prefix=%s" % prefix, 
                          "--without-paraver", 
                          "--without-gui",
                          "--enable-shared"]

        if spec.satisfies('%gcc'):
            configure_args.append('--with-nocross-compiler-suite=gcc')
        if spec.satisfies('%intel'):
            configure_args.append('--with-nocross-compiler-suite=intel')

        configure(*configure_args)

        make(parallel=False)
        make("install", parallel=False)
