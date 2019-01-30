# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Orthomcl(Package):
    """OrthoMCL is a genome-scale algorithm for grouping orthologous protein
       sequences."""

    homepage = "http://orthomcl.org/orthomcl/"
    url      = "http://orthomcl.org/common/downloads/software/v2.0/orthomclSoftware-v2.0.9.tar.gz"

    version('2.0.9', '2e0202ed4e36a753752c3567edb9bba9')

    depends_on('perl', type=('build', 'run'))
    depends_on('blast-plus')
    depends_on('mcl')
    depends_on('mariadb')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('config', prefix.config)
        install_tree('doc', prefix.doc)
        install_tree('lib', prefix.lib)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', self.prefix.lib)
