# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sparsehash(AutotoolsPackage):
    """Sparse and dense hash-tables for C++ by Google"""
    homepage = "https://github.com/sparsehash/sparsehash"
    url      = "https://github.com/sparsehash/sparsehash/archive/sparsehash-2.0.3.tar.gz"

    version('2.0.3', 'd8d5e2538c1c25577b3f066d7a55e99e')
