# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RHighr(RPackage):
    """Provides syntax highlighting for R source code. Currently it supports
    LaTeX and HTML output. Source code of other languages is supported via
    Andre Simon's highlight package."""

    homepage = "https://github.com/yihui/highr"
    url      = "https://cran.r-project.org/src/contrib/highr_0.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/highr"

    version('0.6', 'bf47388c5f57dc61962362fb7e1d8b16')
