# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLazyeval(RPackage):
    """An alternative approach to non-standard evaluation using formulas.
    Provides a full implementation of LISP style 'quasiquotation', making it
    easier to generate code with other code."""

    homepage = "https://cran.r-project.org/web/packages/lazyeval/index.html"
    url      = "https://cran.r-project.org/src/contrib/lazyeval_0.2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lazyeval"

    version('0.2.0', 'df1daac908dcf02ae7e12f4335b1b13b')
