# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Delta(CargoPackage):
    """A syntax-highlighting pager for git"""

    homepage  = "https://github.com/dandavison/delta"
    crates_io = "git-delta"
    git       = "https://github.com/dandavison/delta.git"

    maintainers = ['AndrewGaspar']

    depends_on('llvm@6.0:', type='build', when='@0.0.18:')
    depends_on('oniguruma')

    version('master', branch='master')
    version('0.1.1',  sha256='beb08a0607517a9b16b42c1956ab46e4b12e6bf1f32f6b14306d2b2fefafe24d')

    # delta has a dependency on libclang - specify path to llvm-config
    def setup_build_environment(self, env):
        # onig-sys environment
        env.append_flags('RUSTONIG_DYNAMIC_LIBONIG', '1')
        if '^llvm' in self.spec:
            env.append_flags(
                'LLVM_CONFIG_PATH',
                join_path(self.spec['llvm'].prefix.bin, 'llvm-config'))
