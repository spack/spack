# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bat(CargoPackage):
    """A cat(1) clone with wings."""

    homepage = "https://github.com/sharkdp/bat"
    crates_io = "bat"
    git = "https://github.com/sharkdp/bat.git"

    maintainers = ['AndrewGaspar']

    # onig-sys needs llvm for libclang in order to generate Rust code for onig
    # headers.
    depends_on('llvm@6.0:', type='build', when='@0.13.0:0.15.1')
    depends_on('oniguruma')
    depends_on('libgit2')

    version('master', branch='master')
    version('0.15.4', sha256='91f17c2d9e1cee447a788a15fa6819c0cb488fb2935e3e8c4e7120e1678b7aa8')
    version('0.15.3', sha256='0f7679756b10d2bcff64343cdc6ad93bf19b4ae74d7031b3bd669966b6788fa7')
    version('0.15.2', sha256='1400bbbcbc87fb546db47879009ff61c0b8fd380a3e010830d0ea4d5b1b95aa2')
    version('0.15.1', sha256='655572d855efb05a2f11b0f05dd6edd5ef988ed4df96f4020349ccc2b28f9a24')
    version('0.15.0', sha256='c511711c116f9845e4a8212e21f72c4201414649c9e7e584ab8a68cd0ad2de46')
    version('0.14.0', sha256='d4f3f3e642dcbd5cba51128d99b54ac75872fd3c417bff1ed1a8d08a0c7bac0d')
    version('0.13.0', sha256='738a647b725b5c9901eb356c70c371afa79c8ff7c767c6d318c1f1c94cf1f2f4')
    version('0.12.1', sha256='d1e2f1ea7b1151c99d297f7a4798556f8f96ff30e12c8cc00b3959791be8d39f')
    version('0.12.0', sha256='f870e640d4c052b16d12797cec00a5238258fc62c985ba51117529a72b8a44e2')

    # Tell onig-sys to prefer spack-installed oniguruma
    def setup_build_environment(self, env):
        # onig-sys environment
        env.append_flags('RUSTONIG_DYNAMIC_LIBONIG', '1')
        if '^llvm' in self.spec:
            env.append_flags(
                'LLVM_CONFIG_PATH',
                join_path(self.spec['llvm'].prefix.bin, 'llvm-config'))

        # git-sys environment
        env.append_flags('LIBGIT2_SYS_USE_PKG_CONFIG', '1')
