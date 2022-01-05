# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CircuitBuild(PythonPackage):
    """Command Line API for building circuits"""

    homepage = "https://bbpgitlab.epfl.ch/nse/circuit-build"
    git      = "git@bbpgitlab.epfl.ch:nse/circuit-build.git"

    version('develop', branch='main')
    version('3.1.1', tag='circuit-build-v3.1.1')
    version('3.1.3', tag='circuit-build-v3.1.3')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.99', type='run')
    depends_on('snakemake@5.6:5.99', type='run')
    depends_on('py-pyyaml@5.0:', type='run')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec['snakemake'].prefix.bin)
