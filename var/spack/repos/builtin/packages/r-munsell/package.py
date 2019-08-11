# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMunsell(RPackage):
    """Provides easy access to, and manipulation of, the Munsell colours.
    Provides a mapping between Munsell's original notation (e.g. "5R 5/10") and
    hexadecimal strings suitable for use directly in R graphics. Also provides
    utilities to explore slices through the Munsell colour tree, to transform
    Munsell colours and display colour palettes."""

    homepage = "https://cloud.r-project.org/package=munsell"
    url      = "https://cloud.r-project.org/src/contrib/munsell_0.4.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/munsell"

    version('0.5.0', sha256='d0f3a9fb30e2b5d411fa61db56d4be5733a2621c0edf017d090bdfa5e377e199')
    version('0.4.3', 'ebd205323dc37c948f499ee08be9c476')

    depends_on('r-colorspace', type=('build', 'run'))
