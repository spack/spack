# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ripgrep(Package):
    """ripgrep is a line-oriented search tool that recursively searches
    your current directory for a regex pattern.  ripgrep is similar to
    other popular search tools like The Silver Searcher, ack and grep.
    """

    homepage = "https://github.com/BurntSushi/ripgrep"
    url      = "https://github.com/BurntSushi/ripgrep/archive/11.0.2.tar.gz"

    version('12.1.1', sha256='88d3b735e43f6f16a0181a8fec48847693fae80168d5f889fdbdeb962f1fc804')
    version('12.1.0', sha256='c6bba6d643b1a1f18994683e26d4d2b998b41a7a7360e63cb8ec9db8ffbf793c')
    version('11.0.2', sha256='0983861279936ada8bc7a6d5d663d590ad34eb44a44c75c2d6ccd0ab33490055')

    depends_on('rust')

    def install(self, spec, prefix):
        cargo = which('cargo')
        cargo('install', '--root', prefix, '--path', '.')

    # needed for onig_sys
    def setup_build_environment(self, env):
        env.append_flags('LLVM_CONFIG_PATH',
                         join_path(self.spec['llvm'].prefix.libexec.llvm,
                                   'llvm-config'))
        env.append_flags('LIBCLANG_PATH', self.spec['llvm'].prefix.lib)
