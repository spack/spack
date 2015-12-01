import os

from spack import *
class Adios(Package):
    """The Adaptable IO System (ADIOS) provides a simple, 
        flexible way for scientists to describe the 
        data in their code that may need to be written, 
        read, or processed outside of the running simulation
    """
    
    homepage = "http://www.olcf.ornl.gov/center-projects/adios/"
    url      = "http://users.nccs.gov/~pnorbert/adios-1.9.0.tar.gz"

    version('1.9.0', 'dbf5cb10e32add2f04c9b4052b7ffa76')

    # Lots of setting up here for this package
    # module swap PrgEnv-intel PrgEnv-$COMP
    # module load cray-netcdf/4.3.3.1
    # module load cray-hdf5/1.8.14
    # module load python/2.7.10
    depends_on('mxml')
    
    def install(self, spec, prefix):
        configure_args = ["--prefix=%s" % prefix, 
                          "--with-mxml=%s" % spec['mxml'].prefix, 
                          "--with-hdf5=%s" % os.environ["HDF5_DIR"],
                          "--with-netcdf=%s" % os.environ["NETCDF_DIR"],
                          "--with-infiniband=no",
                          "MPICC=cc","MPICXX=CC","MPIFC=ftn",
                          "CPPFLAGS=-DMPICH_IGNORE_CXX_SEEK"] 

        if spec.satisfies('%gcc'):
            configure_args.extend(["CC=gcc", "CXX=g++", "FC=gfortran"])

        configure(*configure_args)
        make()
        make("install")
