#------------------------------------------------------------------------------
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#------------------------------------------------------------------------------
from spack import *

class PerlExtutilsInstall(Package):
    """Handles the installing and uninstalling of perl modules, scripts, man
    pages, etc...
    """
    homepage = "http://search.cpan.org/~bingos/ExtUtils-Install-2.04/lib/ExtUtils/Install.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/ExtUtils-Install-2.04.tar.gz"

    version('2.04', '5784c74271dcb5f85dd9564e3d3cb726')
    version('2.02', '4c9f7d41a1237ccbc98b9ced1c2d1119')

    depends_on("perl@5.8.1:")

    def install(self, spec, prefix):
        perl = which('perl')
        perl('Makefile.PL',
             'INSTALL_BASE=' + prefix)

        make()
        make("install")

