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
    version('4.0.1', tag='circuit-build-v4.0.1')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.99', type=('build', 'run'))
    depends_on('py-pyyaml@5.0:', type=('build', 'run'))
    depends_on('snakemake@5.10:6.99', type=('build', 'run'))
    depends_on('py-jsonschema@3.2.0:3.99', type=('build', 'run'))
    depends_on('py-jinja2@2.10.0:3.99', type=('build', 'run'))

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec['snakemake'].prefix.bin)
