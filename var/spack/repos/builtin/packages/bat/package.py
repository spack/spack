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

    depends_on('oniguruma')
    depends_on('libgit2')

    version('master', branch='master')
    version('0.13.0', sha256='738a647b725b5c9901eb356c70c371afa79c8ff7c767c6d318c1f1c94cf1f2f4')
    version('0.12.1', sha256='d1e2f1ea7b1151c99d297f7a4798556f8f96ff30e12c8cc00b3959791be8d39f')
    version('0.12.0', sha256='f870e640d4c052b16d12797cec00a5238258fc62c985ba51117529a72b8a44e2')

    # Tell onig-sys to prefer spack-installed oniguruma
    def setup_build_environment(self, env):
        env.append_flags('RUSTONIG_DYNAMIC_LIBONIG', '1')
        env.append_flags('LIBGIT2_SYS_USE_PKG_CONFIG', '1')
