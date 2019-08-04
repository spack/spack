# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RInline(RPackage):
    """Functionality to dynamically define R functions and S4 methods with
    inlined C, C++ or Fortran code supporting .C and .Call calling
    conventions."""

    homepage = "https://cloud.r-project.org/web/packages/inline/index.html"
    url      = "https://cloud.r-project.org/src/contrib/inline_0.3.14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/inline"

    version('0.3.15', sha256='ff043fe13c1991a3b285bed256ff4a9c0ba10bee764225a34b285875b7d69c68')
    version('0.3.14', '9fe304a6ebf0e3889c4c6a7ad1c50bca')
