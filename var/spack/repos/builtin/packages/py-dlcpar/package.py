# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDlcpar(PythonPackage):
    """DLCpar is a reconciliation method for inferring gene duplications,
    losses, and coalescence (accounting for incomplete lineage sorting)."""

    homepage = "https://www.cs.hmc.edu/~yjw/software/dlcpar/"
    url      = "https://www.cs.hmc.edu/~yjw/software/dlcpar/pub/sw/dlcpar-1.0.tar.gz"

    version('2.0.1', sha256='ff30f4e2ade540be1afbf5d6ae75ff64febc9051da734c0f4f3b6abd94a32502')
    version('2.0',   sha256='76ce40d6e6d0c06a7dd0d3064a6d2afdd0b25d848708efb9b0f9309223e5acc0')
    version('1.1',   sha256='61aaf65197d7501bb59659cdc3ac9b13c80aea33c417429a8aff41fa2cd87319')
    version('1.0', sha256='774319caba0f10d1230b8f85b8a147eda5871f9a316d7b3381b91c1bde97aa0a')

    depends_on('py-numpy', type=('build', 'run'))
