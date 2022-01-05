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
    # 0.3.0 > 0.3b > 0.3 as far as Spack is concerned
    version('0.3.0', tag='0.3', preferred=True)
    version('0.3b', commit="c30ea06", submodules=True)
    version('0.3a', commit="86fc52d", submodules=True)
    version('0.2', tag='0.2', submodules=True)

    variant("legacy-unit", default=True, description="Enable legacy units")
    variant("python", default=False, description="Enable python bindings")

    # Build with `ninja` instead of `make`
    generator = 'Ninja'
    depends_on('ninja', type='build')

    depends_on('bison@3.0:3.4.99', when='@:0.3', type='build')
    depends_on('bison@3.0.5:', when='@0.3.1:', type='build')
    depends_on('cmake@3.3.0:', type='build')
    depends_on('flex@2.6:', type='build')
    depends_on('python@3.6.0:')
    depends_on('py-jinja2@2.10:')
    depends_on('py-pytest@4.0.0:')
    depends_on('py-sympy@1.3:')
    depends_on('py-pyyaml@3.13:')

    def cmake_args(self):
        spec = self.spec
        options = []

        if "+python" in spec:
            options.append('-DNMODL_ENABLE_PYTHON_BINDINGS=ON')
        else:
            options.append('-DNMODL_ENABLE_PYTHON_BINDINGS=OFF')

        # installation with pgi fails when debug symbols are added
        if '%pgi' in spec:
            options.append('-DCMAKE_BUILD_TYPE=Release')
        else:
            options.append('-DCMAKE_BUILD_TYPE=RelWithDebInfo')

        if "+legacy-unit" in spec:
            options.append('-DNMODL_ENABLE_LEGACY_UNITS=ON')

        return options

    def setup_build_environment(self, env):
        if '@:0.3b' in self.spec:
            env.prepend_path('PYTHONPATH', self.prefix.lib.python)
        else:
            env.prepend_path('PYTHONPATH', self.prefix.lib)

    def setup_run_environment(self, env):
        if '@:0.3b' in self.spec:
            env.prepend_path('PYTHONPATH', self.prefix.lib.python)
        else:
            env.prepend_path('PYTHONPATH', self.prefix.lib)
