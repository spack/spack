# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPoorman(RPackage):
    """A Poor Man's Dependency Free Recreation of 'dplyr'.

    A replication of key functionality from 'dplyr' and the wider 'tidyverse'
    using only 'base'."""

    cran = "poorman"

    version('0.2.5', sha256='b92b30ce0f4f02c4fa4a4e90673ef2e0ed8de9b9080dd064506581989fcc0716')

    depends_on('r@3.5:', type=('build', 'run'))
