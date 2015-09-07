#------------------------------------------------------------------------------
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#------------------------------------------------------------------------------

from spack import *

class PerlAppCpanminus(Package):
    """cpanminus is a script to get, unpack, build and install modules from
       CPAN and does nothing else.

       It's dependency free (can bootstrap itself), requires zero configuration,
       and stands alone. When running, it requires only 10MB of RAM."""
    homepage = "https://github.com/miyagawa/cpanminus"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/App-cpanminus-1.4004.tar.gz"

    version('1.7039', '3db601cb4902a2646f179f6947b3de28')
    version('1.7038', '3f24ea7f3db9f7fa7bbd41318a52f2b3')
    version('1.7037', '950980f7999e7f9ff0bc4253affffabd')
    version('1.7036', 'b1f33c1f3f7ed0ef0aac2540b70a045a')
    version('1.7035', '2a0c06c619bb77684b57b6912f56fdc8')

    depends_on("perl@5.8:")

    def install(self, spec, prefix):
        perl = which('perl')
        perl('Makefile.PL',
             'PREFIX=' + prefix)

        make()
        make("install")
