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


class Bambam(MakefilePackage):
    """Bambam is a tool used to facilitate NGS analysis."""

    homepage = "http://udall-lab.byu.edu/Research/Software/BamBam"
    url      = "https://downloads.sourceforge.net/project/bambam/bambam-1.4.tgz"

    version('1.4', '4a8a70bd26a68170a97e32bbca15a89f')

    depends_on('perl', type=('build', 'run'))
    depends_on('samtools+old-structure')
    depends_on('bamtools')
    depends_on('htslib')
    depends_on('zlib')

    def edit(self, spec, prefix):
        makefile = FileFilter('makefile')
        makefile.filter('INC = *', 'INC = -I%s ' %
                        self.spec['bamtools'].prefix.include)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('scripts', prefix.scripts)

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('LIBRARY_PATH',
                               self.spec['samtools'].prefix.lib)
        spack_env.prepend_path('LIBRARY_PATH',
                               self.spec['bamtools'].prefix.lib.bamtools)
