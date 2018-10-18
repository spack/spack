# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Charliecloud(MakefilePackage):
    """Lightweight user-defined software stacks for HPC."""

    homepage = "https://hpc.github.io/charliecloud"
    url      = "https://github.com/hpc/charliecloud/archive/v0.2.4.tar.gz"

    version('0.9.3', sha256='f1bf032377b8845bc9a93b8a4fad6386161e35900223c0acc61d1f3aa3a87bc7')
    version('0.9.2', sha256='8d0e4804d412beef720a66f886a0a78bce42f3269e880ebf11f602581f8047d4')
    version('0.9.1', sha256='8e69150a271285da71ece7a09b48251ef6593f72207c5126741d9976aa737d95')
    version('0.9.0', sha256='7e74cb16e31fd9d502198f7509bab14d1049ec68ba90b15e277e76f805db9458')
    version('0.2.4', 'b112de661c2c360174b42c99022c1967')

    @property
    def install_targets(self):
        return ['install', 'PREFIX=%s' % self.prefix]
