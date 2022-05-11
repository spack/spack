# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Mivisionx(CMakePackage):
    """MIVisionX toolkit is a set of comprehensive computer
    vision and machine intelligence libraries, utilities, and
    applications bundled into a single toolkit."""

    homepage = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX"
    git      = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX.git"
    url      = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    def url_for_version(self, version):
        if version == Version('1.7'):
            return "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/archive/1.7.tar.gz"

        url = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/archive/rocm-{0}.tar.gz"
        return url.format(version)

    version('5.1.0', sha256='e082415cc2fb859c53a6d6e5d72ca4529f6b4d56a4abe274dc374faaa5910513')
    version('5.0.2', sha256='da730c2347b7f2d0cb7a262f8305750988f18e9f1eb206cf297bacaab2f6b408')
    version('5.0.0', sha256='935113feb71eced2b5f21fffc2a90a188b4ef2fe009c50f0445504cb27fbc58c')
    version('4.5.2', sha256='26fd7fbd2e319bf4a8657900ad2f81bba1ae66745c2ba95f2f87e33903cfe69c')
    version('4.5.0', sha256='518834893d3fcdb7ecff179b3f3992ca1aacb30b6d95711c74918abb6f80b925')
    version('4.3.1', sha256='d77d63c0f148870dcd2a39a823e94b28adef9e84d2c37dfc3b05db5de4d7af83')
    version('4.3.0', sha256='31f6ab9fb7f40b23d4b24c9a70f809623720943e0492c3d357dd22dcfa50efb2')
    version('4.2.0', sha256='172857b1b340373ae81ed6aa241559aa781e32250e75c82d7ba3c002930a8a3a')
    version('4.1.0', sha256='0b431a49807682b9a81adac6a64160a0712ddaa3963e0f05595c93b92be777ea', deprecated=True)
    version('4.0.0', sha256='e09d4890b729740ded056b3974daea84c8eb1fc93714c52bf89f853c2eef1fb5', deprecated=True)
    version('3.10.0', sha256='8a67fae77a05ef60a501e64a572a7bd2ccb9243518b1414112ccd1d1f78d08c8', deprecated=True)
    version('3.9.0', sha256='892812cc6e6977ed8cd4b69c63f4c17be43b83c78eeafd9549236c17f6eaa2af', deprecated=True)
    version('3.8.0', sha256='4e177a9b5dcae671d6ea9f0686cf5f73fcd1e3feb3c50425c8c6d43ac5d77feb', deprecated=True)
    version('3.7.0', sha256='3ce13c6449739c653139fc121411d94eaa9d764d3d339c4c78fab4b8aa199965', deprecated=True)
    version('1.7', sha256='ff77142fd4d4a93136fd0ac17348861f10e8f5d5f656fa9dacee08d8fcd2b1d8', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')
    variant('backend', default='OPENCL', values=("HIP", "OPENCL"), description='backend type')

    def patch(self):
        if '@4.2.0' in self.spec:
            filter_file('${ROCM_PATH}/opencl',
                        self.spec['rocm-opencl'].prefix,
                        'amd_openvx/cmake/FindOpenCL.cmake',
                        string=True)
            filter_file('/opt/rocm/mivisionx/include',
                        self.spec['mivisionx'].prefix.include,
                        'utilities/mv_deploy/CMakeLists.txt',
                        string=True)
        if '@4.5.0:' in self.spec:
            filter_file('${ROCM_PATH}/miopen',
                        self.spec['miopen-hip'].prefix.miopen,
                        'amd_openvx_extensions/CMakeLists.txt',
                        string=True)
            filter_file('${ROCM_PATH}/bin',
                        self.spec['hip'].prefix.bin,
                        'amd_openvx/openvx/hipvx/CMakeLists.txt',
                        string=True)
            filter_file('${ROCM_PATH}/bin',
                        self.spec['hip'].prefix.bin,
                        'amd_openvx_extensions/amd_nn/nn_hip/CMakeLists.txt',
                        string=True)

    def flag_handler(self, name, flags):
        spec = self.spec
        protobuf = spec['protobuf'].prefix.include
        if name == 'cxxflags':
            flags.append('-I{0}'.format(protobuf))
        return (flags, None, None)

    depends_on('cmake@3.5:', type='build')
    depends_on('ffmpeg@:4', type='build')
    depends_on('protobuf@:3', type='build')
    depends_on('opencv@:3.4 +calib3d+features2d+highgui+imgcodecs+imgproc+video+videoio+flann+photo+objdetect', type='build')
    depends_on('rocm-opencl@3.5.0', when='@1.7')
    depends_on('rocm-cmake@3.5.0', type='build', when='@1.7')
    depends_on('miopen-opencl@3.5.0', when='@1.7')
    depends_on('miopengemm@1.1.6', when='@1.7')
    depends_on('openssl', when='@4.0.0:')
    conflicts('^cmake@3.22:', when='@:5.0.0')

    for ver in ['3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0', '4.2.0',
                '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0',
                '5.0.2', '5.1.0']:
        depends_on('rocm-opencl@' + ver,   when='@' + ver)
        depends_on('miopengemm@' + ver,    when='@' + ver)
        depends_on('miopen-opencl@' + ver, when='@' + ver)
    for ver in ['4.5.0', '4.5.2', '5.0.0', '5.0.2', '5.1.0']:
        depends_on('miopen-hip@' + ver,   when='@' + ver)

    def cmake_args(self):
        spec = self.spec
        protobuf = spec['protobuf'].prefix.include
        args = [
            self.define('CMAKE_CXX_FLAGS', '-I{0}'.format(protobuf)),
            self.define_from_variant('BACKEND', 'backend'),
            self.define('HIP_PATH', spec['hip'].prefix),
            self.define('HSA_PATH', spec['hsa-rocr-dev'].prefix)
        ]
        return args
