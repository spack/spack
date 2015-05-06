# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install netcdf-fortran
#
# You can always get back here to change things with:
#
#     spack edit netcdf-fortran
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class NetcdfFortran(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.4.2.tar.gz"

    version('4.4.2', '1cbad993b2e3673b00f9a5835a547178')


    # requires core netcdf package
    # this package will install into netcdf
    depends_on('netcdf')

    parallel = False

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        # configure("--prefix=%s" % prefix)
        pref = spec['netcdf'].prefix
        configure('--prefix=%s' % pref, 'CPPFLAGS=-I%s/include' % pref, 'LDFLAGS=-L%s/lib' % pref)

        # FIXME: Add logic to build and install here
        make('check')
        make("install")
        outfile = open('%s/placeholder.txt' % prefix, 'w+')
        print >>outfile, 'Netcdf-fortran files are in the netcdf prefix. This is a placeholder or else spack thinks the install failed.'
