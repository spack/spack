# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RProgress(RPackage):
    """Configurable Progress bars, they may include percentage, elapsed time,
       and/or the estimated completion time. They work in terminals, in
       'Emacs' 'ESS', 'RStudio', 'Windows' 'Rgui' and the 'macOS' 'R.app'.
       The package also provides a 'C++' 'API', that works with or without
       'Rcpp'."""

    homepage = "https://cran.r-project.org/package=progress"
    url      = "https://cran.r-project.org/src/contrib/progress_1.1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/progress"

    version('1.1.2', 'b3698672896125137e0077bc97132428')
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-prettyunits', type=('build', 'run'))
