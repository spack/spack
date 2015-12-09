#------------------------------------------------------------------------------
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#------------------------------------------------------------------------------

from spack import *

class PerlAppPerlbrew(Package):
    """An admin-free perl installation management tool"""
    homepage = "http://perlbrew.pl/"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GU/GUGOD/App-perlbrew-0.73.tar.gz"

    version('0.73', '0e83b5ba0e7e65c3f8d1b25fa7f35a97')
    version('0.72', '7b27a67c2dda7009d6900881d57949f6')
    version('0.71', '0b8a3384e63a70da465b67d065ba42d1')
    version('0.70', 'e988420643b572a8f064dd90ed7239a6')
    version('0.69', '5b98462e684c9df6ef875b7f154f397e')

    depends_on("perl@5.8:")

    def install(self, spec, prefix):
        perl = which('perl')
        perl('Makefile.PL',
             'PREFIX=' + prefix)

        make()
        make("install")

