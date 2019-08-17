# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGlue(RPackage):
    """An implementation of interpreted string literals, inspired by Python's
       Literal String Interpolation <https://www.python.org/dev/peps/pep-0498/>
       and Docstrings <https://www.python.org/dev/peps/pep-0257/> and Julia's
       Triple-Quoted String Literals <https://docs.julialang.org/en/stable/
       manual/strings/#triple-quoted-string-literals>."""

    homepage = "https://github.com/tidyverse/glue"
    url      = "https://cran.r-project.org/src/contrib/glue_1.2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/glue"

    version('1.2.0', '77d06b6d86abc882fa1c0599e457c5e2')
