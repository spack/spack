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
    version('0.0.18', sha256='55940e7f571fa89e3e22af026705ba25ed3a9fee1483b5aecb67ba09f1d27975')
    version('0.0.17', sha256='ef44469929eedb4b2f4ad14081b3545608e49eaa000ebdfd6a564d48d0444165')
    version('0.0.16', sha256='3238132f11b7d679cab4b75c1cd8c51ea0eb08e25c60149332aaa6d5f916a6b0')
    version('0.0.15', sha256='775758fa980f90318954ab6fa44803274d1f84da6c8b154a1c2094c8b1c7bf24')
    version('0.0.14', sha256='a9ea255196874f0363c20a88edd28c462cda97e2977cf18c98d0401816dc80b0')
    version('0.0.10', sha256='7f6c0f6f00a7aa6d20ba3aae00aafacdf398d8ffcf6db08493cfc76c2c82ff11')

    # delta has a dependency on libclang - specify path to llvm-config
    def setup_build_environment(self, env):
        # onig-sys environment
        env.append_flags('RUSTONIG_DYNAMIC_LIBONIG', '1')
        if '^llvm' in self.spec:
            env.append_flags(
                'LLVM_CONFIG_PATH',
                join_path(self.spec['llvm'].prefix.bin, 'llvm-config'))
