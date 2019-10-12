# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMass(RPackage):
    """Functions and datasets to support Venables and Ripley, "Modern Applied
    Statistics with S" (4th edition, 2002)."""

    homepage = "https://cloud.r-project.org/package=MASS"
    url      = "https://cloud.r-project.org/src/contrib/MASS_7.3-47.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/MASS"

    version('7.3-51.4', sha256='9911d546a8d29dc906b46cb53ef8aad76d23566f4fc3b52778a1201f8a9b2c74')
    version('7.3-51.3', sha256='5b0e0e7704d43a94b08dcc4b3fe600b9723d1b3e446dd393e82d39ddf66608b6')
    version('7.3-47',   sha256='ed44cdabe84fff3553122267ade61d5cc68071c435f7645d36c8f2e4e9f9c6bf')

    depends_on('r@3.1.0:', type=('build', 'run'))
