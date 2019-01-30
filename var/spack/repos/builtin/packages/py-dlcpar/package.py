# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDlcpar(PythonPackage):
    """DLCpar is a reconciliation method for inferring gene duplications,
    losses, and coalescence (accounting for incomplete lineage sorting)."""

    homepage = "https://www.cs.hmc.edu/~yjw/software/dlcpar/"
    url      = "https://www.cs.hmc.edu/~yjw/software/dlcpar/pub/sw/dlcpar-1.0.tar.gz"

    version('1.0', '0bf684436df3554e46d5e992349eeaec')

    depends_on('py-numpy', type=('build', 'run'))
