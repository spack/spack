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
import glob


class Mitofates(Package):
    """MitoFates predicts mitochondrial presequence, a cleavable localization
       signal located in N-terminal, and its cleaved position."""

    homepage = "http://mitf.cbrc.jp/MitoFates/cgi-bin/top.cgi"
    url      = "http://mitf.cbrc.jp/MitoFates/program/MitoFates_1.2.tar.gz"

    version('1.2', 'aaac42a8e8c7318a4abde9df3a4b72d1')

    depends_on('libsvm')
    depends_on('perl', type='run')
    depends_on('perl-inline-c', type='run')
    depends_on('perl-perl6-slurp', type='run')
    depends_on('perl-math-cephes', type='run')

    # The DirichletRegulator_fast.pm sets the perl Inline directory
    # to be inside the deployed source (which won't be writable by
    # the end user of site wide deployed software.
    # Removing that config entry will cause the inline module to auto
    # create a directory in the user's homedir instead
    patch('DirichletRegulator_fast.patch')

    def patch(self):
        perlscripts = FileFilter('MitoFates.pl')
        perlscripts.filter('#!/usr/bin/perl', '#!/usr/bin/env perl')

        # other perl module files probably should get this filter too
        with working_dir(join_path(self.stage.source_path, 'bin/modules')):
            perlmodules = glob.glob('*.pm')
            filter_file('#!/usr/bin/perl', '#!/usr/bin/env perl', *perlmodules)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install('MitoFates.pl', prefix)
        chmod = which('chmod')
        chmod('+x', join_path(prefix, 'MitoFates.pl'))

    def setup_environment(self, spack_env, run_env):
        # We want the main MitoFates.pl script in the path
        run_env.prepend_path('PATH', self.prefix)
