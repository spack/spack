# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTensora(RPackage):
    """The package provides convenience functions for advance linear algebra
       with tensors and computation with datasets of tensors on a higher level
       abstraction."""

    homepage = "https://cran.r-project.org/web/packages/tensorA/index.html"
    url      = "https://cran.r-project.org/src/contrib/tensorA_0.36.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tensorA"

    version('0.36', '01c0613491d9b46600bf403d7e3bdd80')
