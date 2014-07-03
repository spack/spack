from spack import *

class Tau(Package):
    """A portable profiling and tracing toolkit for performance
       analysis of parallel programs written in Fortran, C, C++, UPC,
       Java, Python."""
    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "http://www.cs.uoregon.edu/research/paracomp/tau/tauprofile/dist/tau-2.23.1.tar.gz"

    versions = { '2.23.1' : '6593b47ae1e7a838e632652f0426fe72', }

    def install(self, spec, prefix):
        # TAU isn't happy with directories that have '@' in the path.  Sigh.
        change_sed_delimiter('@', ';', 'configure')
        change_sed_delimiter('@', ';', 'utils/FixMakefile')
        change_sed_delimiter('@', ';', 'utils/FixMakefile.sed.default')

        # After that, it's relatively standard.
        configure("-prefix=%s" % prefix)
        make("install")
