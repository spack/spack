#------------------------------------------------------------------------------
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#------------------------------------------------------------------------------

from spack import *

class PerlExtutilsMakemaker(Package):
    """(Perl Module) This utility is designed to write a Makefile for an
       extension module from a Makefile.PL. It is based on the Makefile.SH
       model provided by Andy Dougherty and the perl5-porters."""
    homepage = "http://search.cpan.org/~bingos/ExtUtils-MakeMaker-7.06/lib/ExtUtils/MakeMaker.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/ExtUtils-MakeMaker-7.06.tar.gz"

    version('7.07_01', '4177294baff8cc8ad483e58f6c1b8385')
    version('7.06'   , 'd86589e2a88c00c7f0f40dc8d432ecde')
    version('7.05_29', 'dc6a796f78f08eaa5cfa8b36a3053112')
    version('7.05_28', '6182b56cb4c773b60649ca9c6449a331')
    version('7.05_27', '7cb22dcdb477d4aca3dd87deef15e922')

    depends_on("perl@5.8.1:")

    def install(self, spec, prefix):
        perl = which('perl')
        perl('Makefile.PL',
             'INSTALL_BASE=' + prefix)

        make()
        make("install")
