from spack import *
import os

class Nco(Package):
    """The NCO toolkit manipulates and analyzes data stored in
    netCDF-accessible formats"""

    homepage = "https://sourceforge.net/projects/nco"
    url      = "https://github.com/nco/nco/archive/4.5.5.tar.gz"

    version('4.5.5', '9f1f1cb149ad6407c5a03c20122223ce')

    # See "Compilation Requirements" at:
    # http://nco.sourceforge.net/#bld

    depends_on('netcdf')
    depends_on('antlr@2.7.7+cxx')    # (required for ncap2)
    depends_on('gsl')            #  (desirable for ncap2)
    depends_on('udunits2')       # (allows dimensional unit transformations)
    # depends_on('opendap')      # (enables network transparency), 

    def install(self, spec, prefix):
        opts = [
            '--prefix=%s' % prefix,
            '--disable-openmp',    # TODO: Make this a variant
            '--disable-dap',        # TODO: Make this a variant
            '--disable-esmf']
        configure(*opts)
        make()
        make("install")
