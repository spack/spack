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


class Microbiomeutil(MakefilePackage):
    """Microbiome analysis utilities"""

    homepage = "http://microbiomeutil.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/microbiomeutil/microbiomeutil-r20110519.tgz"

    version('20110519', '11eaac4b0468c05297ba88ec27bd4b56')

    depends_on('perl', type=('build', 'run'))
    depends_on('blast-plus')
    depends_on('cdbfasta')

    def install(self, spec, prefix):
        install_tree('ChimeraSlayer', prefix.ChimeraSlayer)
        install_tree('NAST-iEr', join_path(prefix, 'NAST-iEr'))
        install_tree('TreeChopper', prefix.TreeChopper)
        install_tree('WigeoN', prefix.WigeoN)
        install_tree('docs', prefix.docs)
        install_tree('RESOURCES', prefix.resources)
        install_tree('AmosCmp16Spipeline', prefix.AmosCmp16Spipeline)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.ChimeraSlayer)
        run_env.prepend_path('PATH', join_path(self.prefix, 'NAST-iEr'))
        run_env.prepend_path('PATH', self.prefix.TreeChopper)
        run_env.prepend_path('PATH', self.prefix.WigeoN)
