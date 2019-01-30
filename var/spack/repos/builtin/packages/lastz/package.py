# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lastz(MakefilePackage):
    """LASTZ is a program for aligning DNA sequences, a pairwise aligner."""

    homepage = "https://lastz.github.io/lastz"
    url      = "https://github.com/lastz/lastz/archive/1.04.00.tar.gz"

    version('1.04.00', sha256='a4c2c7a77430387e96dbc9f5bdc75874334c672be90f5720956c0f211abf9f5a')

    def install(self, spec, prefix):
        make('install', 'LASTZ_INSTALL={0}'.format(prefix.bin))
