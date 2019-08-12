# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Casper(MakefilePackage):
    """CASPER (Context-Aware Scheme for Paired-End Read) is state-of-the art
       merging tool in terms of accuracy and robustness. Using this
       sophisticated merging method, we could get elongated reads from the
       forward and reverse reads."""

    homepage = "http://best.snu.ac.kr/casper/index.php?name=main"
    url      = "http://best.snu.ac.kr/casper/program/casper_v0.8.2.tar.gz"

    version('0.8.2', '9e83d32ff46b876f33eb1d7b545ec9c2')

    depends_on('jellyfish@2.2.3:')
    depends_on('boost')

    conflicts('%gcc@7.1.0')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.spec.prefix)
