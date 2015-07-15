from spack import *

class Moab(Package):
    """MOAB is a component for representing and evaluating mesh data."""
    homepage = "https://trac.mcs.anl.gov/projects/ITAPS/wiki/MOAB"
    url      = "http://ftp.mcs.anl.gov/pub/fathom/moab-4.6.3.tar.gz"

    version('4.8.1', 'd2adef4e0ea54c6e2c9519b23aab91bd')
    version('4.8.0', '795aa3777d50918d155ed388bc042e6c')
    version('4.6.3', '3cc9be3e5f347a2e8a9a15f1978be58e')
    version('4.6.2', '1450594ff4f4e0c8393859dfcfde74fb')
    version('4.6.1', '67827abd5d4fd4cd584699d8a24578a1')

    depends_on("cgm")
    depends_on("hdf5")
    depends_on("zoltan_distrib")
    depends_on("parmetis")
    depends_on("netcdf")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "CC=cc",  
                  "CFLAGS=-static", 
                  "CXX=CC", 
                  "CXXFLAGS=-static", 
                  "--disable-shared",
                  "--with-mpi", 
                  "--with-cgm=%s" % spec['cgm'].prefix, 
                  "--enable-igeom", 
                  "--with-hdf5=%s" % spec['hdf5'].prefix, 
                  "--with-zoltan=%s" % spec['zoltan_distrib'].prefix, 
                  "--with-parmetis=%s" % spec['parmetis'].prefix, 
                  "--with-netcdf=%s" % spec['netcdf'].prefix, 
                  "--disable-fortran")

        make()
        make("install")
