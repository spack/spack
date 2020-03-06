# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bat(Package):
    """A cat(1) clone with wings."""

    homepage = "https://github.com/sharkdp/bat"
    url      = "https://github.com/sharkdp/bat/archive/v0.10.0.tar.gz"

    version('0.12.1', sha256='1dd184ddc9e5228ba94d19afc0b8b440bfc1819fef8133fe331e2c0ec9e3f8e2')

    depends_on('rust')

    def install(self, spec, prefix):
        cargo = which('cargo')
        cargo('install', '--root', prefix, '--path', '.')

    # cargo seems to need these to be set so that when it's building
    # onig_sys it can run llvm-config and link against libclang.
    def setup_build_environment(self, env):
        env.append_flags('LLVM_CONFIG_PATH',
                         join_path(self.spec['llvm'].prefix.libexec.llvm,
                                   'llvm-config'))
        env.append_flags('LIBCLANG_PATH', self.spec['llvm'].prefix.lib)
