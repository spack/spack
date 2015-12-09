from spack import *

import os
from glob import glob

from llnl.util.filesystem import join_path, mkdirp

class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://www.kernel.org/pub/software/scm/git/git-2.2.1.tar.xz"

    version('2.2.1', '43e01f9d96ba8c11611e0eef0d9f9f28')

    # Use system openssl.
    # depends_on("openssl")

    depends_on("zlib")

    #-------------------------------------------------------------------------
    # Dependency - Perl::ExtUtils::MakeMaker
    #-------------------------------------------------------------------------
    #
    # Required to address make error:
    #
    #    GEN git-instaweb
    #        Can't locate ExtUtils/MakeMaker.pm in @INC ...
    #    make[1]: *** [perl.mak] Error 2
    #    make: *** [perl/perl.mak] Error 2
    depends_on("Perl-ExtUtils-MakeMaker")

    #-------------------------------------------------------------------------
    # Dependency - Perl::ExtUtils::Install
    #-------------------------------------------------------------------------
    #
    # Required to address make error:
    #
    #   SUBDIR perl
    #       Can't locate ExtUtils/Install.pm in @INC ...
    #   make[2]: *** [pm_to_blib] Error 2
    depends_on("Perl-ExtUtils-Install")

    def install(self, spec, prefix):
        # Add Perl::ExtUtils::MakeMaker to PERL5LIB
        # Add Perl::ExtUtils::Install to PERL5LIB
        ExtUtils_MakeMaker = spec['Perl-ExtUtils-MakeMaker']
        ExtUtils_Install = spec['Perl-ExtUtils-Install']
        os.environ['PERL5LIB'] = \
            ''.join(glob(join_path(ExtUtils_MakeMaker.prefix.lib, "site_perl/*"))) + ':' + \
            ''.join(glob(join_path(ExtUtils_Install.prefix.lib, "site_perl/*"))) + ':' +   \
            os.getenv('PERL5LIB', '')

        configure("--prefix=%s" % prefix,
                  "--without-python")

        make()
        make("install")
