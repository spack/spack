# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RDeoptim(RPackage):
    """Implements the differential evolution algorithm for global optimization
    of a real-valued function of a real-valued parameter vector."""

    homepage = "https://cran.r-project.org/package=DEoptim"
    url      = "https://cran.r-project.org/src/contrib/DEoptim_2.2-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DEoptim"

    version('2.2-3', 'ed406e6790f8f1568aa9bec159f80326')
