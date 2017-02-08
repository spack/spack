##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
#
# Author: George Hartzell <hartzell@alerce.com>
# Date: July 21, 2016
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#
from spack import *


class Perl(Package):
    """Perl 5 is a highly capable, feature-rich programming language with over
       27 years of development."""
    homepage = "http://www.perl.org"
    url      = "http://www.cpan.org/src/5.0/perl-5.24.1.tar.gz"

    version('5.24.1', '765ef511b5b87a164e2531403ee16b3c')
    version('5.24.0', 'c5bf7f3285439a2d3b6a488e14503701')
    version('5.22.2', '5767e2a10dd62a46d7b57f74a90d952b')
    version('5.20.3', 'd647d0ea5a7a8194c34759ab9f2610cd')
    # 5.18.4 fails with gcc-5
    # https://rt.perl.org/Public/Bug/Display.html?id=123784
    # version('5.18.4' , '1f9334ff730adc05acd3dd7130d295db')

    # Installing cpanm alongside the core makes it safe and simple for
    # people/projects to install their own sets of perl modules.  Not
    # having it in core increases the "energy of activation" for doing
    # things cleanly.
    variant('cpanm', default=True,
            description='Optionally install cpanm with the core packages.')

    resource(
        name="cpanm",
        url="http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/App-cpanminus-1.7042.tar.gz",
        md5="e87f55fbcb3c13a4754500c18e89219f",
        destination="cpanm",
        placement="cpanm"
    )

    def install(self, spec, prefix):
        configure = Executable('./Configure')
        configure("-des", "-Dprefix=" + prefix)
        make()
        if self.run_tests:
            make("test")
        make("install")

        if '+cpanm' in spec:
            with working_dir(join_path('cpanm', 'cpanm')):
                perl = Executable(join_path(prefix.bin, 'perl'))
                perl('Makefile.PL')
                make()
                make('install')
