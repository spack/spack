# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ripgrep(CargoPackage):
    """ripgrep is a line-oriented search tool that recursively searches
    your current directory for a regex pattern.  ripgrep is similar to
    other popular search tools like The Silver Searcher, ack and grep.
    """

    homepage = "https://github.com/BurntSushi/ripgrep"
    url      = "https://crates.io/api/v1/crates/ripgrep/12.0.1/download"

    version('12.0.1', sha256='7dc6e92652933ac66d236d78ef61658b73c09639981bd1be0630461ce64d3cab', extension='tar.gz')
    version('11.0.2', sha256='d903146d825e92f77f95d1e1e8e5272f42253978c07d58c2294467a14dca126f', extension='tar.gz')
    version('11.0.1', sha256='bafda49e418a8cd7df1fddddab809beb131117c698dc120ca614019b3e05c42e', extension='tar.gz')
    version('0.10.0', sha256='7f3ab77309993175ac2fe01a7f990bf972c0ddae0d63d747693d598bfaf2de44', extension='tar.gz')
    version('0.3.1',  sha256='0f37b342258640323b43d50ffb72a972dfe8cb4bd28d3b8f40d1da0ffdb21987', extension='tar.gz')
    # version('11.0.2', sha256='0983861279936ada8bc7a6d5d663d590ad34eb44a44c75c2d6ccd0ab33490055')

    # depends_on('rust')

    # def install(self, spec, prefix):
    #     cargo = which('cargo')
    #     cargo('install', '--root', prefix, '--path', '.')

    # # needed for onig_sys
    # def setup_build_environment(self, env):
    #     env.append_flags('LLVM_CONFIG_PATH',
    #                      join_path(self.spec['llvm'].prefix.libexec.llvm,
    #                                'llvm-config'))
    #     env.append_flags('LIBCLANG_PATH', self.spec['llvm'].prefix.lib)
