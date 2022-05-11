# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RRgenoud(RPackage):
    """R Version of GENetic Optimization Using Derivatives.

    A genetic algorithm plus derivative optimizer."""

    cran = "rgenoud"

    version('5.8-3.0', sha256='9beb11b5edab3ab3aa6001daa39668b240a8e0328be9d55db4e23ff88ce3235d')
    version('5.8-2.0', sha256='106c4f6a6df5159578e929a0141b3cfbaa88141a70703ff59a1fc48a27e2d239')
    version('5.8-1.0', sha256='9deca354be6887f56bf9f4ca9a7291296050e51149ae9a3b757501704126c38a')

    depends_on('r@2.15:', type=('build', 'run'))
