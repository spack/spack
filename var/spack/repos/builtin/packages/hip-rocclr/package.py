# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class HipRocclr(CMakePackage):
    """Hip-ROCclr is a virtual device interface that compute runtimes interact
       with to different backends such as ROCr or PAL This abstraction allows
       runtimes to work on Windows as well as on Linux without much effort."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCclr"
    git      = "https://github.com/ROCm-Developer-Tools/ROCclr.git"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    def url_for_version(self, version):
        # Fix up a typo in the 3.5.0 release.
        if version == Version('3.5.0'):
            return "https://github.com/ROCm-Developer-Tools/ROCclr/archive/roc-3.5.0.tar.gz"

        url = "https://github.com/ROCm-Developer-Tools/ROCclr/archive/rocm-{0}.tar.gz"
        return url.format(version)

    version('master', branch='develop')
    version('4.5.2', sha256='6581916a3303a31f76454f12f86e020fb5e5c019f3dbb0780436a8f73792c4d1')
    version('4.5.0', sha256='ca8d6305ff0e620d9cb69ff7ac3898917db9e9b6996a7320244b48ab6511dd8e')
    version('4.3.1', sha256='bda52c65f03a69a9d8ab1a118d45646d76843249fb975d67e5141e63fa3acc79')
    version('4.3.0', sha256='8a86b4f2a1b1c7ac628262e5b11b07ff42a224e62e594a4e0683aeb616062538')
    version('4.2.0', sha256='c57525af32c59becf56fd83cdd61f5320a95024d9baa7fb729a01e7a9fcdfd78')
    version('4.1.0', sha256='9eb1d88cfc9474979aaf29b99bcf9d3769a0f7f1f8f10660941aabf83d9eeb0c', deprecated=True)
    version('4.0.0', sha256='8db502d0f607834e3b882f939d33e8abe2f9b55ddafaf1b0c2cd29a0425ed76a', deprecated=True)
    version('3.10.0', sha256='d1ac02840c2dcb3d5fa3008fe9e313767ebe6d1dcf978a924341834ec96ebfe2', deprecated=True)
    version('3.9.0', sha256='d248958672ae35ab7f9fbd83827ccf352e2756dfa7819f6b614ace2e1a9a064e', deprecated=True)
    version('3.8.0', sha256='10d8aa6f5af7b51813015da603c4e75edc863c3530793f6ed9769ca345c08ed6', deprecated=True)
    version('3.7.0', sha256='a49f464bb2eab6317e87e3cc249aba3b2517a34fbdfe50175f0437f69a219adc', deprecated=True)
    version('3.5.0', sha256='87c1ee9f02b8aa487b628c543f058198767c474cec3d21700596a73c028959e1', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('mesa~llvm@21:', type='link')
    depends_on('libelf', type='link', when="@3.7.0:3.8.0")
    depends_on('numactl', type='link', when="@3.7.0:")

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', 'master']:
        depends_on('hsakmt-roct@' + ver, when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)
        depends_on('comgr@' + ver, when='@' + ver)

    # See: https://github.com/ROCm-Developer-Tools/ROCclr/pull/16
    # In 3.7.0 the find opengl things have changed slightly.
    patch('opengl.patch', when='@3.5.0')

    resource(name='opencl-on-vdi',
             url='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz',
             sha256='511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0',
             expand=True,
             destination='',
             placement='opencl-on-vdi',
             when='@3.5.0')

    # Add opencl sources thru the below
    for d_version, d_shasum in [
        ('4.5.2',  '96b43f314899707810db92149caf518bdb7cf39f7c0ad86e98ad687ffb0d396d'),
        ('4.5.0',  '3a163aed24619b3faf5e8ba17325bdcedd1667a904ea20914ac6bdd33fcdbca8'),
        ('4.3.1',  '7f98f7d4707b4392f8aa7017aaca9e27cb20263428a1a81fb7ec7c552e60c4ca'),
        ('4.3.0',  'd37bddcc6835b6c0fecdf4d02c204ac1d312076f3eef2b1faded1c4c1bc651e9'),
        ('4.2.0',  '18133451948a83055ca5ebfb5ba1bd536ed0bcb611df98829f1251a98a38f730'),
        ('4.1.0',  '0729e6c2adf1e3cf649dc6e679f9cb936f4f423f4954ad9852857c0a53ef799c'),
        ('4.0.0',  'd43ea5898c6b9e730b5efabe8367cc136a9260afeac5d0fe85b481d625dd7df1'),
        ('3.10.0', '3aa9dc5a5f570320b04b35ee129ce9ff21062d2770df934c6c307913f975e93d'),
        ('3.9.0',  '286ff64304905384ce524cd8794c28aee216befd6c9267d4187a12e5a21e2daf'),
        ('3.8.0',  '7f75dd1abf3d771d554b0e7b0a7d915ab5f11a74962c92b013ee044a23c1270a'),
        ('3.7.0',  '283e1dfe4c3d2e8af4d677ed3c20e975393cdb0856e3ccd77b9c7ed2a151650b')
    ]:
        resource(
            name='opencl-on-vdi',
            url='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz'.format(d_version),
            sha256=d_shasum,
            expand=True,
            destination='',
            placement='opencl-on-vdi',
            when='@{0}'.format(d_version)
        )

    resource(
        name='opencl-on-vdi',
        git='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git',
        destination='',
        placement='opencl-on-vdi',
        branch='main',
        when='@master'
    )

    @property
    def install_targets(self):
        if self.spec.satisfies('@4.5.0:'):
            return []
        return ['install']

    @run_after('install')
    def deploy_missing_files(self):
        if '@3.5.0' in self.spec:
            # the amdrocclr_staticTargets.cmake file is generated but not
            # installed and when we install it by hand, we have to fix the
            # path to the static library libamdrocclr_static.a from build
            # dir to prefix lib dir.
            cmakefile = join_path(self.build_directory,
                                  'amdrocclr_staticTargets.cmake')
            filter_file(self.build_directory, self.prefix.lib, cmakefile)
            install(cmakefile, self.prefix.lib)
        elif self.spec.satisfies('@3.7.0:4.3.2'):
            path = join_path(self.prefix.lib,
                             'cmake/rocclr/ROCclrConfig.cmake')
            filter_file(self.build_directory, self.prefix, path)

    def cmake_args(self):
        args = [
            '-DUSE_COMGR_LIBRARY=yes',
            '-DOPENCL_DIR={0}/opencl-on-vdi'.format(self.stage.source_path)
        ]
        return args
