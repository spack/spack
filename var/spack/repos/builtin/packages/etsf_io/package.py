from spack import *

class EtsfIo(Package):
    """ETSF_IO is a library implementing the Nanoquanta / ETSF file format specifications.
    
    ETSF_IO enables an architecture-independent exchange of crystallographic data, 
    electronic wavefunctions, densities and potentials, as well as spectroscopic data. 
    It is meant to be used by quantum-physical and quantum-chemical applications relying 
    upon the Density Functional Theory (DFT) framework."""

    homepage = "http://www.etsf.eu/resources/software/libraries_and_tools"
    url      = "https://launchpad.net/etsf-io/1.0/1.0.4/+download/etsf_io-1.0.4.tar.gz"

    version('1.0.4', '32d0f7143278bd925b334c69fa425da1')

    depends_on("netcdf-fortran")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]
        oapp = options.append
        #--with-netcdf-incs=-I/Users/gmatteo/local/include 
        #--with-netcdf-libs=-L/Users/gmatteo/local/lib -lnetcdff -lnetcdf 
        #-L/Users/gmatteo/local/lib -lhdf5_hl -lhdf5 
        #--with-moduledir=/Users/gmatteo/Software/abinit/803/gmatteo-training/build_gcc/fallbacks/exports/include

        hdf_libs = "-L%s -lhdf5_hl -lhdf5" % spec["hdf"].prefix.lib  
        options.extend([
            "--with-netcdf-incs=-I%s" % spec["netcdf-fortran"].prefix.include,
            "--with-netcdf-libs=-L%s -lnetcdff -lnetcdf" % (spec["netcdf-fortran"].prefix.lib, hdf_libs),
        ])

        configure(*options)

        make()
        make("install")
