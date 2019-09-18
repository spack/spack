# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RBitops(RPackage):
    """Functions for bitwise operations on integer vectors."""

    homepage = "https://cloud.r-project.org/package=bitops"
    url      = "https://cloud.r-project.org/src/contrib/bitops_1.0-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bitops"

    version('1.0-6', 'fba16485a51b1ccd354abde5816b6bdd')
