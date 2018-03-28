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


class Guidance(MakefilePackage):
    """Guidance: Accurate detection of unreliable alignment regions accounting
       for the uncertainty of multiple parameters."""

    homepage = "http://guidance.tau.ac.il/ver2/"
    url      = "http://guidance.tau.ac.il/ver2/guidance.v2.02.tar.gz"

    version('2.02', 'aa6ae2168e8e0237ee56bc2ac81202cf')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-bio-perl', type=('build', 'run'))
    depends_on('ruby')
    depends_on('prank')
    depends_on('clustalw')
    depends_on('mafft')
    depends_on('muscle')

    conflicts('%gcc@6.2.0:')

    def edit(self, spec, prefix):
        for dir in 'Guidance', 'Selecton', 'bioSequence_scripts_and_constants':
            with working_dir(join_path('www', dir)):
                files = glob.iglob('*.pl')
                for file in files:
                    perl = FileFilter(file)
                    perl.filter('#!/usr/bin/perl -w', '#!/usr/bin/env perl')

    def install(self, spac, prefix):
        mkdir(prefix.bin)
        install_tree('libs', prefix.bin.libs)
        install_tree('programs', prefix.bin.programs)
        install_tree('www', prefix.bin.www)
        with working_dir(join_path('www', 'Guidance')):  # copy without suffix
            install('guidance.pl', join_path(prefix.bin.www.Guidance,
                                             'guidance'))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', prefix.bin.www.Guidance)
