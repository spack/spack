from spack import *

class Ncview(Package):
    """Simple viewer for NetCDF files."""
    homepage = "http://meteora.ucsd.edu/~pierce/ncview_home_page.html"
    url      = "ftp://cirrus.ucsd.edu/pub/ncview/ncview-2.1.7.tar.gz"

    version('2.1.7', 'debd6ca61410aac3514e53122ab2ba07')

    depends_on("netcdf")
    depends_on("udunits2")

    # OS Dependencies
    # Ubuntu: apt-get install libxaw7-dev
    # CentOS 7: yum install libXaw-devel

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
