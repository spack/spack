# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hyphen(AutotoolsPackage):
    """A library of text hyphenation."""

    homepage = "http://hunspell.github.io"
    url      = "http://downloads.sourceforge.net/hunspell/hyphen-2.8.8.tar.gz"

    version('2.8.8', sha256='304636d4eccd81a14b6914d07b84c79ebb815288c76fe027b9ebff6ff24d5705')
