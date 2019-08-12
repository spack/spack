# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
