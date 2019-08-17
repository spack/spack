# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Prodigal(MakefilePackage):
    """Fast, reliable protein-coding gene prediction for prokaryotic
    genomes."""

    homepage = "https://github.com/hyattpd/Prodigal"
    url      = "https://github.com/hyattpd/Prodigal/archive/v2.6.3.tar.gz"

    version('2.6.3', '5181809fdb740e9a675cfdbb6c038466')

    def install(self, spec, prefix):
        make('INSTALLDIR={0}'.format(self.prefix), 'install')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', prefix)
