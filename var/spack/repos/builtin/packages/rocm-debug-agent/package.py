# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class RocmDebugAgent(CMakePackage):
    """Radeon Open Compute (ROCm) debug agent"""

    homepage = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent"
    git      = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent.git"
    url      = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('5.0.2', sha256='4ec3cdedc4ba774d05c3dc972186b3181b3aa823af08f3843238961d5ef90e57')
    version('5.0.0', sha256='fb8ebe136bfa815116453bdcb4afb9617ab488f54501434c72eed9706857be3f')
    version('4.5.2', sha256='85c7f19485defd9a58716fffdd1a0e065ed7f779c3f124467fca18755bc634a6')
    version('4.5.0', sha256='6486b1a8515da4711d3c85f8e41886f8fe6ba37ca2c63664f00c811f6296ac20')
    version('4.3.1', sha256='7bee6be6c29883f03f47a8944c0d50b7cf43a6b5eeed734602f521c3c40a18d0')
    version('4.3.0', sha256='0cdee5792b808e03b839070da0d1b08dc4078a7d1fc295f0c99c6a5ae7d636a6')
    version('4.2.0', sha256='ce02a5b752291882daa0a2befa23944e59087ce9fe65a91061476c3c399e4a0c')
    version('4.1.0', sha256='b1ae874887e5ee037070f1dd46b145ad02ec9fd8a724c6b6ae194b534f01acdb', deprecated=True)
    version('4.0.0', sha256='a9e64834d56a9221c242e71aa110c2cef0087aa8f86f50428dd618e5e623cc3c', deprecated=True)
    version('3.10.0', sha256='675b8d3cc4aecc4428a93553abf664bbe6a2cb153f1f480e6cadeeb4d24ef4b1', deprecated=True)
    version('3.9.0', sha256='3e56bf8b2b53d9102e8709b6259deea52257dc6210df16996b71a7d677952b1b', deprecated=True)
    version('3.8.0', sha256='55243331ac4b0d90e88882eb29fd06fad354e278f8a34ac7f0680b2c895ca2ac', deprecated=True)
    version('3.7.0', sha256='d0f442a2b224a734b0080c906f0fc3066a698e5cde9ff97ffeb485b36d2caba1', deprecated=True)
    version('3.5.0', sha256='203ccb18d2ac508aae40bf364923f67375a08798b20057e574a0c5be8039f133', deprecated=True)

    def url_for_version(self, version):
        url = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent/archive/"
        if version <= Version('3.7.0'):
            url += "roc-{0}.tar.gz".format(version)
        else:
            url += "rocm-{0}.tar.gz".format(version)

        return url

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('elfutils@:0.168', type='link')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2']:
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)
        depends_on('hsakmt-roct@' + ver, when='@' + ver)

    for ver in ['3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0', '4.2.0',
                '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2']:
        depends_on('rocm-dbgapi@' + ver, when='@' + ver)
        depends_on('hip@' + ver, when='@' + ver)

    # https://github.com/ROCm-Developer-Tools/rocr_debug_agent/pull/4
    patch('0001-Drop-overly-strict-Werror-flag.patch', when='@3.7.0:')
    patch('0002-add-hip-architecture.patch', when='@3.9.0:')

    @property
    def root_cmakelists_dir(self):
        if '@3.5.0' in self.spec:
            return 'src'
        else:
            return self.stage.source_path

    def cmake_args(self):
        spec = self.spec
        args = []

        if '@3.5.0' in spec:
            args.append(
                '-DCMAKE_PREFIX_PATH={0}/include/hsa;{1}/include,'.
                format(spec['hsa-rocr-dev'].prefix, spec['hsakmt-roct'].prefix)
            )

        if '@3.7.0:' in spec:
            args.append(
                '-DCMAKE_MODULE_PATH={0}'.
                format(spec['hip'].prefix.cmake)
            )
        return args
