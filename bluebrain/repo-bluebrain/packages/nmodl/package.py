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

    # 0.3.1 > 0.3.0.20220110 > 0.3.0 > 0.3b > 0.3 to Spack
    version('develop', branch='master', submodules=True)
    version('llvm', branch='llvm', submodules=True)
    # For deployment; nmodl@0.3.0%nvhpc@21.11 doesn't build with eigen/intrinsics errors
    version('0.3.0.20220110', commit='9e0a6f260ac2e6fad068a39ea3bdf7aa7a6f4ee0')
    version('0.3.0', tag='0.3')
    version('0.3b', commit="c30ea06", submodules=True)
    version('0.3a', commit="86fc52d", submodules=True)
    version('0.2', tag='0.2', submodules=True)

    variant("legacy-unit", default=True, description="Enable legacy units")
    variant("python", default=False, description="Enable python bindings")
    variant("llvm", default=False, description="Enable llvm codegen")
    variant("llvm_cuda", default=False, description="Enable llvm codegen with CUDA backend")

    # Build with `ninja` instead of `make`
    generator = 'Ninja'
    depends_on('ninja', type='build')
    depends_on('llvm', when='+llvm')
    depends_on('cuda', when='+llvm_cuda')

    conflicts('+llvm', when='@0.2:0.3.0.20220110', msg='cannot enable LLVM backend outside of llvm version')
    conflicts('+llvm_cuda', when='@0.2:0.3.0.20220110', msg='cannot enable CUDA LLVM backend outside of llvm version')

    # 0.3b includes #270 and #318 so should work with bison 3.6+
    depends_on('bison@3.0:3.4.99', when='@:0.3a', type='build')
    depends_on('bison@3.0.5:', when='@0.3b:', type='build')
    depends_on('cmake@3.17.0:', when='@llvm', type='build')
    depends_on('cmake@3.15.0:', when='@0.3.0.20220110:', type='build')
    depends_on('cmake@3.3.0:', when='@:0.3', type='build')
    depends_on('flex@2.6:', type='build')
    depends_on('python@3.6.0:')
    depends_on('py-jinja2@2.10:')
    depends_on('py-pytest@4.0.0:')
    depends_on('py-sympy@1.3:1.8')
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

        if "+llvm" in spec:
            options.append('-DNMODL_ENABLE_LLVM=ON')
        else:
            options.append('-DNMODL_ENABLE_LLVM=OFF')

        if "+llvm_cuda" in spec:
            options.append('-DNMODL_ENABLE_LLVM_CUDA=ON')

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
