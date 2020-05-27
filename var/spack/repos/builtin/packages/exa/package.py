# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exa(CargoPackage):
    """A modern replacement for ls"""

    homepage  = "https://the.exa.website/"
    crates_io = "exa"
    git       = "https://github.com/ogham/exa.git"

    maintainers = ['AndrewGaspar']

    # exa doesn't build with prefer_dynamic at present, so switch default to
    # False
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )

    depends_on('libgit2')

    def setup_build_environment(self, env):
        env.append_flags('LIBGIT2_SYS_USE_PKG_CONFIG', '1')

    version('master', branch='master')
    version('0.9.0', sha256='0463ccb5038bd6a0ee042e0a8ff5cd9792906e19a29f0ce631217c7a5f1720e9')
    version('0.8.0', sha256='4291b26960413bfa2d7c682644b18aeadb0ff9182ec0d980cf22806b8d3bb6a4')
