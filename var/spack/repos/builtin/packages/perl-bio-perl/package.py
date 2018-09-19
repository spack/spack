##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
