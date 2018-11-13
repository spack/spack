# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRlang(RPackage):
    """A toolbox for working with base types, core R features like the
       condition system, and core 'Tidyverse' features like tidy evaluation."""

    homepage = "https://cran.r-project.org/package=rlang"
    url      = "https://cran.r-project.org/src/contrib/rlang_0.2.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rlang"

    version('0.2.2', 'df2abf3a1936c503ed1edd4350ffb5f0')
    version('0.1.4', 'daed5104d557c0cbfb4a654ec8ffb579')
    version('0.1.2', '170f8cf7b61898040643515a1746a53a')
    version('0.1.1', '38a51a0b8f8487eb52b4f3d986313682')
