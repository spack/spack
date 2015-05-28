from spack import *

class Cgm(Package):
    """The Common Geometry Module, Argonne (CGMA) is a code library which provides geometry functionality used for mesh generation and other applications."""
    homepage = "http://trac.mcs.anl.gov/projects/ITAPS/wiki/CGM"
    url      = "http://ftp.mcs.anl.gov/pub/fathom/cgm13.1.1.tar.gz"

    version('13.1.1', '4e8dbc4ba8f65767b29f985f7a23b01f')
    version('13.1.0', 'a6c7b22660f164ce893fb974f9cb2028')
    version('13.1'  , '95f724bda04919fc76818a5b7bc0b4ed')

    depends_on("openmpi")

    def install(self, spec, prefix):
        configure("--with-mpi",
                "--prefix=%s" % prefix, 
                "CFLAGS=-static", 
                "CXXFLAGS=-static", 
                "FCFLAGS=-static") 

        make()
        make("install")
