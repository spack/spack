# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Last(MakefilePackage):
    """LAST finds similar regions between sequences, and aligns them. It is
       designed for comparing large datasets to each other (e.g. vertebrate
       genomes and/or large numbers of DNA reads)."""

    homepage = "http://last.cbrc.jp/"
    url      = "http://last.cbrc.jp/last-869.zip"

    version('869', '12dced14418fb924a1b0604593274973')

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix)
