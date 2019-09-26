# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Maverick(MakefilePackage):
    """MavericK is a program for inferring population structure on the basis
       of genetic information."""

    homepage = "https://github.com/bobverity/MavericK"
    url      = "https://github.com/bobverity/MavericK/archive/v1.0.4.tar.gz"

    version('1.0.4', '0c17c9a73fd0ac0aef17339173ddedc2')

    conflicts('%gcc@:6.0')
    conflicts('%cce')
    conflicts('%clang')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('MavericK', prefix.bin)
