##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Vcftools(AutotoolsPackage):
    """VCFtools is a program package designed for working with VCF files,
       such as those generated by the 1000 Genomes Project. The aim of
       VCFtools is to provide easily accessible methods for working
       with complex genetic variation data in the form of VCF files.
    """

    homepage = "https://vcftools.github.io/"
    url      = "https://github.com/vcftools/vcftools/releases/download/v0.1.14/vcftools-0.1.14.tar.gz"

    # this is "a pre-release"
    # version('0.1.15', '61045197848dea20a0158d2faf02e5be')
    version('0.1.14', 'a110662535651caa6cc8c876216a9f77')

    depends_on('perl', type=('build', 'run'))
    depends_on('zlib')

    # this needs to be in sync with what setup_environment adds to
    # PERL5LIB below
    def configure_args(self):
        return ['--with-pmdir=lib']

    @run_before('install')
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
           can fix up the path to the perl binary.
        """

        with working_dir('src/perl'):
            match = '^#!/usr/bin/env perl'
            perl = join_path(self.spec['perl'].prefix.bin, 'perl')
            substitute = "#!{perl}".format(perl=perl)
            # tab-to-vcf added in 0.1.15
            files = ['fill-aa', 'fill-an-ac', 'fill-fs',
                     'fill-ref-md5', 'tab-to-vcf', 'vcf-annotate',
                     'vcf-compare', 'vcf-concat', 'vcf-consensus',
                     'vcf-contrast', 'vcf-convert',
                     'vcf-fix-newlines', 'vcf-fix-ploidy',
                     'vcf-indel-stats', 'vcf-isec', 'vcf-merge',
                     'vcf-phased-join', 'vcf-query',
                     'vcf-shuffle-cols', 'vcf-sort', 'vcf-stats',
                     'vcf-subset', 'vcf-to-tab', 'vcf-tstv',
                     'vcf-validator', ]
            kwargs = {'ignore_absent': True, 'backup': False, 'string': False}
            filter_file(match, substitute, *files, **kwargs)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', join_path(self.prefix, 'lib'))
