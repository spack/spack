# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
       create portable applications for AMD and NVIDIA GPUs from
       single source code."""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP"
    url      = "https://github.com/ROCm-Developer-Tools/HIP/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='ae8384362986b392288181bcfbe5e3a0ec91af4320c189bd83c844ed384161b3')

    depends_on('cmake@3:', type='build')
    depends_on('perl@5.10:', type=('build', 'run'))
    for ver in ['3.5.0']:
        depends_on('rocclr@' + ver,  type='build', when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('rocminfo@' + ver, type='build', when='@' + ver)
        depends_on('mesa~llvm@18.3:', type=('build', 'link'), when='@' + ver)

    # Note: the ROCm ecosystem expects `lib/` and `bin/` folders with symlinks
    # in the parent directory of the package, which is incompatible with spack.
    # In hipcc the ROCM_PATH variable is used to point to the parent directory
    # of the package. With the following patch we should never hit code that
    # uses the ROCM_PATH variable again; just to be sure we set it to an empty
    # string.
    patch('0001-Make-it-possible-to-specify-the-package-folder-of-ro.patch', when='@3.5.0')

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2141
    patch('0002-Fix-detection-of-HIP_CLANG_ROOT.patch', when='@3.5.0')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('ROCM_PATH', '')
        env.set('HIP_COMPILER', 'clang')
        env.set('HIP_PLATFORM', 'hcc')
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        env.set('HSA_PATH', self.spec['hsa-rocr-dev'].prefix)
        env.set('ROCMINFO_PATH', self.spec['rocminfo'].prefix)
        env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, 'hipcc')

    def patch(self):
        filter_file(
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/../include"',
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"',
            'hip-config.cmake.in', string=True)

    @run_before('install')
    def filter_sbang(self):
        perl = self.spec['perl'].command
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

        with working_dir('bin'):
            match = '^#!/usr/bin/perl'
            substitute = "#!{perl}".format(perl=perl)
            files = [
                'hipify-perl', 'hipcc', 'extractkernel',
                'hipconfig', 'hipify-cmakefile'
            ]
            filter_file(match, substitute, *files, **kwargs)

    def cmake_args(self):
        args = [
            '-DHIP_COMPILER=clang',
            '-DHIP_PLATFORM=rocclr',
            '-DHSA_PATH={0}'.format(self.spec['hsa-rocr-dev'].prefix),
            '-DLIBROCclr_STATIC_DIR={0}/lib'.format(self.spec['rocclr'].prefix)
        ]
        return args
