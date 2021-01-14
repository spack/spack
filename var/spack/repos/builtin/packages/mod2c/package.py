##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Mod2c(CMakePackage):

    """MOD2C is NMODL to C converter adapted for CoreNEURON simulator.
    More information about NMODL can be found NEURON simulator
    documentation at Yale University."""

    homepage = "https://github.com/BlueBrain/mod2c"
    url      = "https://github.com/BlueBrain/mod2c.git"

    version('develop', git=url, preferred=True)

    depends_on('cmake@2.8.12:', type='build')

    def cmake_args(self):
        spec = self.spec
        options = []
        if 'bgq' in spec.architecture and '%xl' in spec:
            options.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        return options

    def setup_run_environment(self, env):
        env.set('MODLUNIT', join_path(self.prefix, 'share/nrnunits.lib'))
