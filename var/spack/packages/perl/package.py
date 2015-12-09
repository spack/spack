#------------------------------------------------------------------------------
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#------------------------------------------------------------------------------
from spack import *

class Perl(Package):
    """Perl 5 is a highly capable, feature-rich programming language with over
       27 years of development."""
    homepage = "http://www.cpan.org/src/"
    url      = "http://www.cpan.org/src/5.0/perl-5.22.0.tar.gz"

    # Note: Even minor version numbers are stable releases
    version('5.22.0' , 'e32cb6a8dda0084f2a43dac76318d68d')

    def install(self, spec, prefix):
        configure = Executable('./Configure')
        configure("-des",
                  "-Dprefix=" + prefix)
        make()
        make("install")
