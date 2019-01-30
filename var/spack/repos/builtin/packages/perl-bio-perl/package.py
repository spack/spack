# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import inspect


class PerlBioPerl(PerlPackage):
    """Functional access to BioPerl for people who don't know objects"""

    homepage = "http://search.cpan.org/~cjfields/BioPerl-1.007002/Bio/Perl.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/C/CJ/CJFIELDS/BioPerl-1.007002.tar.gz"

    version('1.007002', 'a912c92b56d009198f1786b4cf560d5c')

    depends_on('perl-module-build', type='build')
    depends_on('perl-uri-escape', type=('build', 'run'))
    depends_on('perl-io-string', type=('build', 'run'))
    depends_on('perl-data-stag', type=('build', 'run'))
    depends_on('perl-test-most', type=('build', 'run'))

    def configure(self, spec, prefix):
        # Overriding default configure method in order to cater to interactive
        # Build.pl
        self.build_method = 'Build.PL'
        self.build_executable = Executable(
            join_path(self.stage.source_path, 'Build'))

        # Config questions consist of:
        #    Do you want to run the Bio::DB::GFF or Bio::DB::SeqFeature::Store
        #        live database tests? y/n [n]
        #
        #    Install [a]ll BioPerl scripts, [n]one, or choose groups
        #        [i]nteractively? [a]
        #
        #    Do you want to run tests that require connection to servers across
        #        the internet (likely to cause some failures)? y/n [n]
        #
        # Eventually, someone can add capability for the other options, but
        # the current answers are the most practical for a spack install.

        config_answers = ['n\n', 'a\n', 'n\n']
        config_answers_filename = 'spack-config.in'

        with open(config_answers_filename, 'w') as f:
            f.writelines(config_answers)

        with open(config_answers_filename, 'r') as f:
            inspect.getmodule(self).perl('Build.PL', '--install_base=%s' %
                                         self.prefix, input=f)
