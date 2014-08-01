# FIXME: Add copyright statement here 

from spack import *

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

    version('1.1.2', '9a262c7ca05ff0ab5f7775ae96f3539e')

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix,
                  "--enable-shared")

        # FIXME: Add logic to build and install here
        make()
        make("install")
