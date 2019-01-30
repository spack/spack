# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RShape(RPackage):
    """Functions for plotting graphical shapes such as ellipses, circles,
       cylinders, arrows, ..."""

    homepage = "https://cran.r-project.org/package=shape"
    url      = "https://cran.r-project.org/src/contrib/shape_1.4.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/shape"

    version('1.4.3', '2a807bf95e7decc71478f805221852da')
    version('1.4.2', '75557c43a385b9cc0c4dff361af6e06c')
