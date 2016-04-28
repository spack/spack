from spack import *

class Cfitsio(Package):
    """
    CFITSIO is a library of C and Fortran subroutines for reading and writing
    data files in FITS (Flexible Image Transport System) data format.
    """
    homepage = 'http://heasarc.gsfc.nasa.gov/fitsio/'
    version('3.370', 'abebd2d02ba5b0503c633581e3bfa116')

    def url_for_version(self, v):
        url = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio{0}.tar.gz'
        return url.format(str(v).replace('.', ''))

    def install(self, spec, prefix):
        configure('--prefix=' + prefix)
        make()
        make('install')
