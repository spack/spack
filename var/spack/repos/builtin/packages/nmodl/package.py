# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nmodl(CMakePackage):
    """Code Generation Framework For NEURON MODeling Language """

    homepage = "https://github.com/BlueBrain/nmodl.git"
    url      = "https://github.com/BlueBrain/nmodl.git"
    git      = "https://github.com/BlueBrain/nmodl.git"

    version('develop', branch='master', submodules=True)
    version('0.3', commit="86fc52d2", submodules=True)
    version('0.2', tag='0.2', submodules=True)

    depends_on('bison@3.0:3.4.99', when='@:0.3', type='build')
    depends_on('bison@3.0:', when='@0.3.1:', type='build')
    depends_on('cmake@3.3.0:', type='build')
    depends_on('flex@2.6:', type='build')
    depends_on('python@3.6.0:')
    depends_on('py-jinja2@2.7:')
    depends_on('py-pytest@3.0:')
    depends_on('py-sympy@1.2:')
    depends_on('py-pyyaml@3.13:')

    def setup_build_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix.lib.python)

    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix.lib.python)
