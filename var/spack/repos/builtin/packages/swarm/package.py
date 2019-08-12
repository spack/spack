# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Swarm(MakefilePackage):
    """A robust and fast clustering method for amplicon-based studies."""

    homepage = "https://github.com/torognes/swarm"
    url      = "https://github.com/torognes/swarm/archive/v2.1.13.tar.gz"

    version('2.1.13', 'ab6aff0ba5d20a53b9f13f8f3d85839f')

    build_directory = 'src'

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('scripts', prefix.scripts)
        install_tree('man', prefix.share.man)
