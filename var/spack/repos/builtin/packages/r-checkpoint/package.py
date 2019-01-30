# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCheckpoint(RPackage):
    """The goal of checkpoint is to solve the problem of package
    reproducibility in R. Specifically, checkpoint allows you to
    install packages as they existed on CRAN on a specific snapshot
    date as if you had a CRAN time machine."""

    homepage = "https://cran.r-project.org/package=checkpoint"
    url      = "https://cran.r-project.org/src/contrib/checkpoint_0.3.18.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/checkpoint"

    version('0.3.18', '021d7faeb72c36167951e103b2b065ea')
    version('0.3.15', 'a4aa8320338f1434a330d984e97981ea')

    depends_on('r@3.0.0:')
