# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RoctracerDev(CMakePackage):
    """ROC-tracer library: Runtimes Generic Callback/Activity APIs.
       The goal of the implementation is to provide a generic independent from
       specific runtime profiler to trace API and asyncronous activity."""

    homepage = "https://github.com/ROCm-Developer-Tools/roctracer"
    git      = "https://github.com/ROCm-Developer-Tools/roctracer.git"
    url      = "https://github.com/ROCm-Developer-Tools/roctracer/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    version('4.3.1', sha256='88ada5f256a570792d1326a305663e94cf2c3b0cbd99f7e745326923882dafd2')
    version('4.3.0', sha256='c3d9f408df8d4dc0e9c0026217b8c684f68e775da80b215fecb3cd24419ee6d3')
    version('4.2.0', sha256='62a9c0cb1ba50b1c39a0636c886ac86e75a1a71cbf5fec05801517ceb0e67a37')
    version('4.1.0', sha256='5d93de4e92895b6eb5f9d098f5dbd182d33923bd9b2ab69cf5a1abbf91d70695')
    version('4.0.0', sha256='f47859a46173228b597c463eda850b870e810534af5efd5f2a746067ef04edee')
    version('3.10.0', sha256='ac4a1d059fc34377e906071fd0e56f5434a7e0e4ded9db8faf9217a115239dec')
    version('3.9.0', sha256='0678f9faf45058b16923948c66d77ba2c072283c975d167899caef969169b292')
    version('3.8.0', sha256='5154a84ce7568cd5dba756e9508c34ae9fc62f4b0b5731f93c2ad68b21537ed1')
    version('3.7.0', sha256='6fa5b771e990f09c242237ab334b9f01039ec7d54ccde993e719c5d6577d1518')
    version('3.5.0', sha256='7af5326c9ca695642b4265232ec12864a61fd6b6056aa7c4ecd9e19c817f209e')

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('python@:2', type='build', when='@:4.1.0')
    depends_on('python@3:', type='build', when='@4.2.0:')
    depends_on('py-cppheaderparser', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('hsakmt-roct@' + ver, when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)
        depends_on('rocminfo@' + ver, when='@' + ver)
        depends_on('hip@' + ver, when='@' + ver)

    for ver in ['4.2.0', '4.3.0', '4.3.1']:
        depends_on('rocprofiler-dev@' + ver, when='@' + ver)

    def setup_build_environment(self, build_env):
        spec = self.spec
        build_env.set("HIP_PATH", spec['hip'].prefix)

    def patch(self):
        filter_file('${CMAKE_PREFIX_PATH}/hsa',
                    '${HSA_RUNTIME_INC_PATH}', 'src/CMakeLists.txt',
                    string=True)
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        with working_dir('script'):
            match = '^#!/usr/bin/python[23]'
            python = self.spec['python'].command.path
            substitute = "#!{python}".format(python=python)
            files = [
                'check_trace.py', 'gen_ostream_ops.py', 'hsaap.py', 'kfdap.py'
            ]
            filter_file(match, substitute, *files, **kwargs)

    def cmake_args(self):
        args = ['-DHIP_VDI=1',
                '-DCMAKE_MODULE_PATH={0}/cmake_modules'.format(
                    self.stage.source_path),
                '-DHSA_RUNTIME_HSA_INC_PATH={0}/include'.format(
                    self.spec['hsa-rocr-dev'].prefix)
                ]
        return args
