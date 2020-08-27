# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyShakemap(PythonPackage):
    """ShakeMap is a system for rapidly characterizing the extent nad
    distribution of strong ground shaking following
    significant earthquakes."""

    homepage = "http://usgs.github.io/shakemap/"
    url      = "https://github.com/usgs/shakemap/archive/4.0.2.tar.gz"

    version('4.0.2', sha256='52a7f640d4ff98a99703d7d9564fcf3437d0cd23cac5e6ba23d88b17db6c580d')
    version('4.0.1', sha256='fa1a7a994aaa1217b3a3892acabdc4f3ccd15500abd0b0b4449e85ab8312681b')
    version('4.0.0', sha256='65e73c56a09239c0fa83f31f430ccae983bb0748e25f98ad67a22d0f26e0b50d')
    version('0.91',  sha256='548a64c0433225217625e85c9321a0df3f0b586fb6e0ced2767731d2f9349468')
    version('0.9',   sha256='8de233d3dfd3ef94e6680805a265f6c8845540c0fb2b5671ede64de97ec47a33')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
