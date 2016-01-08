from spack import *

class R(Package):
    """R is 'GNU S', a freely available language and environment for
       statistical computing and graphics which provides a wide va
       riety of statistical and graphical techniques: linear and
       nonlinear modelling, statistical tests, time series analysis,
       classification, clustering, etc. Please consult the R project
       homepage for further information."""
    homepage = "http://www.example.com"
    url      = "http://cran.cnr.berkeley.edu/src/base/R-3/R-3.1.2.tar.gz"

    version('3.1.2', '3af29ec06704cbd08d4ba8d69250ae74')

    depends_on("readline")
    depends_on("ncurses")
    depends_on("icu")
    depends_on("glib")
    depends_on("zlib")
    depends_on("libtiff")
    depends_on("jpeg")
    depends_on("cairo")
    depends_on("pango")
    depends_on("freetype")
    depends_on("tcl")
    depends_on("tk")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--enable-R-shlib",
                  "--enable-BLAS-shlib")
        make()
        make("install")
