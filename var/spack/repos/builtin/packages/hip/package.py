# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.hooks.sbang import filter_shebang
from spack.package_defs import *
from spack.util.prefix import Prefix


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
       create portable applications for AMD and NVIDIA GPUs from
       single source code."""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP"
    git      = "https://github.com/ROCm-Developer-Tools/HIP.git"
    url      = "https://github.com/ROCm-Developer-Tools/HIP/archive/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']
    version('master', branch='master')
    version('5.1.0', sha256='47e542183699f4005c48631d96f6a1fbdf27e07ad3402ccd7b5f707c2c602266')
    version('5.0.2', sha256='e23601e6f4f62083899ea6356fffbe88d1deb20fa61f2c970e3c0474cd8886ca')
    version('5.0.0', sha256='ae12fcda2d955f04a51c9e794bdb0fa96539cda88b6de8e377850e68e7c2a781')
    version('4.5.2', sha256='c2113dc3c421b8084cd507d91b6fbc0170765a464b71fb0d96bb875df368f160')
    version('4.5.0', sha256='4026f31fb4f8050e9aa9d4294f29c3410bfb38422dbbae4236ccd65fed4d55b2')
    version('4.3.1', sha256='955311193819f487f9a2d64bffe07c4b8c3a0dc644dc3ad984f7c66a325bdd6f')
    version('4.3.0', sha256='293b5025b5e153f2f25e465a2e0006a2b4606db7b7ec2ae449f8a4c0b52d491b')
    version('4.2.0', sha256='ecb929e0fc2eaaf7bbd16a1446a876a15baf72419c723734f456ee62e70b4c24')
    version('4.1.0', sha256='e21c10b62868ece7aa3c8413ec0921245612d16d86d81fe61797bf9a64bc37eb', deprecated=True)
    version('4.0.0', sha256='d7b78d96cec67c55b74ea3811ce861b16d300410bc687d0629e82392e8d7c857', deprecated=True)
    version('3.10.0', sha256='0082c402f890391023acdfd546760f41cb276dffc0ffeddc325999fd2331d4e8', deprecated=True)
    version('3.9.0', sha256='25ad58691456de7fd9e985629d0ed775ba36a2a0e0b21c086bd96ba2fb0f7ed1', deprecated=True)
    version('3.8.0', sha256='6450baffe9606b358a4473d5f3e57477ca67cff5843a84ee644bcf685e75d839', deprecated=True)
    version('3.7.0', sha256='757b392c3beb29beea27640832fbad86681dbd585284c19a4c2053891673babd', deprecated=True)
    version('3.5.0', sha256='ae8384362986b392288181bcfbe5e3a0ec91af4320c189bd83c844ed384161b3', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3.16.8:', type='build', when='@4.5.0:')
    depends_on('cmake@3.4.3:', type='build')
    depends_on('perl@5.10:', type=('build', 'run'))
    depends_on('gl@4.5:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('hip-rocclr@' + ver, when='@' + ver)
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0']:
        depends_on('hsakmt-roct@' + ver, when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)
        depends_on('comgr@' + ver, when='@' + ver)
        depends_on('llvm-amdgpu@{0} +rocm-device-libs'.format(ver), when='@' + ver)
        depends_on('rocminfo@' + ver, when='@' + ver)
        depends_on('roctracer-dev-api@' + ver, when='@' + ver)

    # hipcc likes to add `-lnuma` by default :(
    # ref https://github.com/ROCm-Developer-Tools/HIP/pull/2202
    depends_on('numactl', when='@3.7.0:')

    # Add hip-amd sources thru the below
    for d_version, d_shasum in [
        ('5.1.0', '77984854bfe00f938353fe4c7604d09967eaf5c609d05f1e6423d3c3dea86e61'),
        ('5.0.2', '80e7268dd22eba0f2f9222932480dede1d80e56227c0168c6a0cc8e4f23d3b76'),
        ('5.0.0', 'cbd95a577abfd7cbffee14a4848f7789a417c6e5e5a713f42eb75d7948abcdf9'),
        ('4.5.2', 'b6f35b1a1d0c466b5af28e26baf646ae63267eccc4852204db1e0c7222a39ce2'),
        ('4.5.0', '7b93ab64d6894ff9b5ba0be35e3ed8501d6b18a2a14223d6311d72ab8a9cdba6')
    ]:
        resource(
            name='hipamd',
            url='https://github.com/ROCm-Developer-Tools/hipamd/archive/rocm-{0}.tar.gz'.format(d_version),
            sha256=d_shasum,
            expand=True,
            destination='',
            placement='hipamd',
            when='@{0}'.format(d_version)
        )
    # Add opencl sources thru the below
    for d_version, d_shasum in [
        ('5.1.0',  '362d81303048cf7ed5d2f69fb65ed65425bc3da4734fff83e3b8fbdda51b0927'),
        ('5.0.2',  '3edb1992ba28b4a7f82dd66fbd121f62bd859c1afb7ceb47fa856bd68feedc95'),
        ('5.0.0',  '2aa3a628b336461f83866c4e76225ef5338359e31f802987699d6308515ae1be'),
        ('4.5.2',  '96b43f314899707810db92149caf518bdb7cf39f7c0ad86e98ad687ffb0d396d'),
        ('4.5.0',  '3a163aed24619b3faf5e8ba17325bdcedd1667a904ea20914ac6bdd33fcdbca8')
    ]:
        resource(
            name='opencl',
            url='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz'.format(d_version),
            sha256=d_shasum,
            expand=True,
            destination='',
            placement='opencl',
            when='@{0}'.format(d_version)
        )
    for d_version, d_shasum in [
        ('5.1.0',  'f4f265604b534795a275af902b2c814f416434d9c9e16db81b3ed5d062187dfa'),
        ('5.0.2',  '34decd84652268dde865f38e66f8fb4750a08c2457fea52ad962bced82a03e5e'),
        ('5.0.0',  '6b72faf8819628a5c109b2ade515ab9009606d10f11316f0d7e4c4c998d7f724'),
        ('4.5.2',  '6581916a3303a31f76454f12f86e020fb5e5c019f3dbb0780436a8f73792c4d1'),
        ('4.5.0',  'ca8d6305ff0e620d9cb69ff7ac3898917db9e9b6996a7320244b48ab6511dd8e')
    ]:
        resource(
            name='rocclr',
            url='https://github.com/ROCm-Developer-Tools/ROCclr/archive/rocm-{0}.tar.gz'.format(d_version),
            sha256=d_shasum,
            expand=True,
            destination='',
            placement='rocclr',
            when='@{0}'.format(d_version)
        )
    # Note: the ROCm ecosystem expects `lib/` and `bin/` folders with symlinks
    # in the parent directory of the package, which is incompatible with spack.
    # In hipcc the ROCM_PATH variable is used to point to the parent directory
    # of the package. With the following patch we should never hit code that
    # uses the ROCM_PATH variable again; just to be sure we set it to an empty
    # string.
    patch('0001-Make-it-possible-to-specify-the-package-folder-of-ro.patch', when='@3.5.0:4.5.3')
    patch('0010-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host.5.0.0.patch', when='@5.0.0')
    patch('0011-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host.5.0.2.patch', when='@5.0.2:')

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2141
    patch('0002-Fix-detection-of-HIP_CLANG_ROOT.patch', when='@:3.9.0')

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2218
    patch('0003-Improve-compilation-without-git-repo.3.7.0.patch', when='@3.7.0:3.9.0')
    patch('0003-Improve-compilation-without-git-repo.3.10.0.patch', when='@3.10.0:4.0.0')
    patch('0003-Improve-compilation-without-git-repo.4.1.0.patch', when='@4.1.0')
    patch('0003-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host.4.2.0.patch', when='@4.2.0:4.3.2')
    patch('0009-Improve-compilation-without-git-repo-and-remove-compiler-rt-linkage-for-host_disabletests.4.5.0.patch', when='@4.5.0:4.5.3')
    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2219
    patch('0004-Drop-clang-rt-builtins-linking-on-hip-host.3.7.0.patch', when='@3.7.0:3.9.0')
    patch('0004-Drop-clang-rt-builtins-linking-on-hip-host.3.10.0.patch', when='@3.10.0:4.1.0')

    # Tests are broken when using cmake 3.21
    with when('^cmake@3.21.0:'):
        patch('0005-Disable-tests-3.5.0.patch', when='@3.5.0')
        patch('0005-Disable-tests-3.6.0.patch', when='@3.6.0:3.8.0')
        patch('0005-Disable-tests-3.9.0.patch', when='@3.9.0:4.0.0')
        patch('0005-Disable-tests-4.1.0.patch', when='@4.1.0:4.3.2')

    patch('Add_missing_open_cl_header_file_for_4.3.0.patch', when='@4.3.0:4.3.2')

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies('@:4.3.2'):
            return self.stage.source_path
        else:
            return 'hipamd'

    def get_paths(self):
        if self.spec.external:
            # For external packages we only assume the `hip` prefix is known,
            # because spack does not set prefixes of dependencies of externals.
            # We assume self.spec.prefix is /opt/rocm-x.y.z/hip and rocm has a
            # default installation with everything installed under
            # /opt/rocm-x.y.z
            rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))

            if not os.path.isdir(rocm_prefix):
                msg = "Could not determine prefix for other rocm components\n"
                msg += "Either report a bug at github.com/spack/spack or "
                msg += "manually edit rocm_prefix in the package file as "
                msg += "a workaround."
                raise RuntimeError(msg)

            paths = {
                'rocm-path': rocm_prefix,
                'llvm-amdgpu': rocm_prefix.llvm,
                'hsa-rocr-dev': rocm_prefix.hsa,
                'rocminfo': rocm_prefix,
                'rocm-device-libs': rocm_prefix
            }
        else:
            paths = {
                'rocm-path': self.spec.prefix,
                'llvm-amdgpu': self.spec['llvm-amdgpu'].prefix,
                'hsa-rocr-dev': self.spec['hsa-rocr-dev'].prefix,
                'rocminfo': self.spec['rocminfo'].prefix,
                'rocm-device-libs': self.spec['llvm-amdgpu'].prefix
            }

        if '@:3.8.0' in self.spec:
            paths['bitcode'] = paths['rocm-device-libs'].lib
        else:
            paths['bitcode'] = paths['rocm-device-libs'].amdgcn.bitcode

        return paths

    def set_variables(self, env):
        # Note: do not use self.spec[name] here, since not all dependencies
        # have defined prefixes when hip is marked as external.
        paths = self.get_paths()

        # Used in hipcc, but only useful when hip is external, since only then
        # there is a common prefix /opt/rocm-x.y.z.
        env.set('ROCM_PATH', paths['rocm-path'])

        # hipcc recognizes HIP_PLATFORM == hcc and HIP_COMPILER == clang, even
        # though below we specified HIP_PLATFORM=rocclr and HIP_COMPILER=clang
        # in the CMake args.
        if self.spec.satisfies('@:4.0.0'):
            env.set('HIP_PLATFORM', 'hcc')
        else:
            env.set('HIP_PLATFORM', 'amd')

        env.set('HIP_COMPILER', 'clang')

        # bin directory where clang++ resides
        env.set('HIP_CLANG_PATH', paths['llvm-amdgpu'].bin)

        # Path to hsa-rocr-dev prefix used by hipcc.
        env.set('HSA_PATH', paths['hsa-rocr-dev'])

        # This is a variable that does not exist in hipcc but was introduced
        # in a patch of ours since 3.5.0 to locate rocm_agent_enumerator:
        # https://github.com/ROCm-Developer-Tools/HIP/pull/2138
        env.set('ROCMINFO_PATH', paths['rocminfo'])

        # This one is used in hipcc to run `clang --hip-device-lib-path=...`
        env.set('DEVICE_LIB_PATH', paths['bitcode'])

        # And this is used in clang whenever the --hip-device-lib-path is not
        # used (e.g. when clang is invoked directly)
        env.set('HIP_DEVICE_LIB_PATH', paths['bitcode'])

        # Just the prefix of hip (used in hipcc)
        env.set('HIP_PATH', paths['rocm-path'])

        # Used in comgr and seems necessary when using the JIT compiler, e.g.
        # hiprtcCreateProgram:
        # https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/blob/rocm-4.0.0/lib/comgr/src/comgr-env.cpp
        env.set('LLVM_PATH', paths['llvm-amdgpu'])

        # Finally we have to set --rocm-path=<prefix> ourselves, which is not
        # the same as --hip-device-lib-path (set by hipcc). It's used to set
        # default bin, include and lib folders in clang. If it's not set it is
        # infered from the clang install dir (and they try to find
        # /opt/rocm again...). If this path is set, there is no strict checking
        # and parsing of the <prefix>/bin/.hipVersion file. Let's just set this
        # to the hip prefix directory for non-external builds so that the
        # bin/.hipVersion file can still be parsed.
        # See also https://github.com/ROCm-Developer-Tools/HIP/issues/2223
        if '@3.8.0:' in self.spec:
            env.append_path('HIPCC_COMPILE_FLAGS_APPEND',
                            '--rocm-path={0}'.format(paths['rocm-path']),
                            separator=' ')

    def setup_build_environment(self, env):
        self.set_variables(env)

    def setup_run_environment(self, env):
        self.set_variables(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.set_variables(env)

        if 'amdgpu_target' in dependent_spec.variants:
            arch = dependent_spec.variants['amdgpu_target']
            if 'none' not in arch and 'auto' not in arch:
                env.set('HCC_AMDGPU_TARGET', ','.join(arch.value))

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_dependent_build_environment(env, dependent_spec)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, 'hipcc')

    def patch(self):
        if self.spec.satisfies('@:4.3.2'):
            filter_file(
                'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/../include"',
                'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"',
                'hip-config.cmake.in', string=True)

        perl = self.spec['perl'].command
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

        with working_dir('bin'):
            match = '^#!/usr/bin/perl'
            substitute = "#!{perl}".format(perl=perl)

            if self.spec.satisfies('@:4.0.0'):
                files = [
                    'hipify-perl', 'hipcc', 'extractkernel',
                    'hipconfig', 'hipify-cmakefile'
                ]
            elif self.spec.satisfies('@4.0.0:4.3.2'):
                files = [
                    'hipify-perl', 'hipcc', 'roc-obj-extract',
                    'hipconfig', 'hipify-cmakefile',
                    'roc-obj-ls', 'hipvars.pm'
                ]
            elif self.spec.satisfies('@4.5.0:'):
                files = []
            filter_file(match, substitute, *files, **kwargs)
            # This guy is used during the cmake phase, so we have to fix the
            # shebang already here in case it is too long.
            filter_shebang('hipconfig')
        if self.spec.satisfies('@4.5.0:'):
            perl = self.spec['perl'].command
            kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
            with working_dir('hipamd/bin'):
                match = '^#!/usr/bin/perl'
                substitute = "#!{perl}".format(perl=perl)
                files = [
                    'roc-obj-extract', 'roc-obj-ls'
                ]
                filter_file(match, substitute, *files, **kwargs)
        if '@3.7.0:' in self.spec:
            numactl = self.spec['numactl'].prefix.lib
            kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

            with working_dir('bin'):
                match = ' -lnuma'
                substitute = " -L{numactl} -lnuma".format(numactl=numactl)
                filter_file(match, substitute, 'hipcc', **kwargs)

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and self.spec.satisfies('@3.7.0:4.3.2'):
            incl = self.spec['hip-rocclr'].prefix.include
            flags.append('-I {0}/compiler/lib/include'.format(incl))
            flags.append('-I {0}/elf'.format(incl))

        return (flags, None, None)

    def cmake_args(self):
        args = [
            self.define('PROF_API_HEADER_PATH', join_path(
                        self.spec['roctracer-dev-api'].prefix,
                        'roctracer', 'inc', 'ext')),
            self.define('HIP_COMPILER', 'clang'),
            self.define('HSA_PATH', self.spec['hsa-rocr-dev'].prefix)
        ]
        if self.spec.satisfies('@:4.0.0'):
            args.append(self.define('HIP_RUNTIME', 'ROCclr'))
            args.append(self.define('HIP_PLATFORM', 'rocclr'))
        else:
            args.append(self.define('HIP_RUNTIME', 'rocclr'))
            args.append(self.define('HIP_PLATFORM', 'amd'))

        # LIBROCclr_STATIC_DIR is unused from 3.6.0 and above
        if '@3.5.0:4.3.2' in self.spec:
            args.append(self.define('LIBROCclr_STATIC_DIR',
                        self.spec['hip-rocclr'].prefix.lib))
        if '@4.5.0:' in self.spec:
            args.append(self.define('HIP_COMMON_DIR', self.stage.source_path))
            args.append(self.define('HIP_CATCH_TEST', 'OFF'))
            args.append(self.define('ROCCLR_PATH', self.stage.source_path + '/rocclr'))
            args.append(self.define('AMD_OPENCL_PATH',
                                    self.stage.source_path + '/opencl'))

        return args
