# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sniffles(CMakePackage):
    """Structural variation caller using third generation sequencing."""

    homepage = "https://github.com/fritzsedlazeck/Sniffles/wiki"
    url      = "https://github.com/fritzsedlazeck/Sniffles/archive/v1.0.5.tar.gz"

    version('1.0.7', '83bd93c5ab5dad3a6dc776f11d3a880e')
    version('1.0.5', 'c2f2350d00418ba4d82c074e7f0b1832')

    # the build process doesn't actually install anything, do it by hand
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        src = "bin/sniffles-core-{0}".format(spec.version.dotted)
        binaries = ['sniffles', 'sniffles-debug']
        for b in binaries:
            install(join_path(src, b), join_path(prefix.bin, b))
