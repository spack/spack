# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Starship(CargoPackage):
    """The minimal, blazing-fast, and infinitely customizable prompt for any
    shell!
    """

    homepage = "https://starship.rs/"
    crates_io = "starship"
    git = "https://github.com/starship/starship.git"

    maintainers = ["AndrewGaspar"]

    # Change the defaults for prefer_dynamic and lto to reflect that starship
    # cannot build with prefer_dynamic at this time, and prefers to be built
    # with lto.
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )

    variant(
        'lto',
        default='fat',
        description='Link binaries with link-time optimization',
        values=('none', 'thin', 'fat')
    )

    depends_on('pkgconfig', type='build')
    depends_on('libgit2')

    def setup_build_environment(self, env):
        env.append_flags('LIBGIT2_SYS_USE_PKG_CONFIG', '1')

    version('master', branch='master')
    version('0.43.0', sha256='8ae08e37c960a62130af61e37bf1f6c4703f277a42dcf0cdeea4955c8d049a6e')
