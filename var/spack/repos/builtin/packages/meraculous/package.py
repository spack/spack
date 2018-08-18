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


class Meraculous(CMakePackage):
    """Meraculous is a while genome assembler for Next Generation Sequencing
       data geared for large genomes."""

    homepage = "http://jgi.doe.gov/data-and-tools/meraculous/"
    url      = "https://downloads.sourceforge.net/project/meraculous20/Meraculous-v2.2.4.tar.gz"
    git      = "https://bitbucket.org/berkeleylab/genomics-meraculous2.git"

    version('2.2.5.1', branch='release-2.2.5.1')
    version('2.2.4', '349feb6cb178643a46e4b092c87bad3a')

    depends_on('perl', type=('build', 'run'))
    depends_on('boost@1.5.0:')
    depends_on('gnuplot@3.7:')
    depends_on('perl-log-log4perl', type=('build', 'run'))

    conflicts('%gcc@6.0.0:', when='@2.2.4')

    def patch(self):
        edit = FileFilter('CMakeLists.txt')
        edit.filter("-static-libstdc\+\+", "")

    def setup_environment(self, spack_env, run_env):
        run_env.set('MERACULOUS_ROOT', self.prefix)
        run_env.prepend_path('PERL5LIB', self.prefix.lib)
