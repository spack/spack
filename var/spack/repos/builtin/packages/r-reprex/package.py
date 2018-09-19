##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RReprex(RPackage):
    """Convenience wrapper that uses the 'rmarkdown' package to render small
       snippets of code to target formats that include both code and output.
       The goal is to encourage the sharing of small, reproducible, and
       runnable examples on code-oriented websites, such as
       <http://stackoverflow.com> and <https://github.com>, or in email.
       'reprex' also extracts clean, runnable R code from various common
       formats, such as copy/paste from an R session."""

    homepage = "https://github.com/jennybc/reprex"
    url      = "https://cran.r-project.org/src/contrib/reprex_0.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/reprex"

    version('0.1.1', 'fcd89995d7b35a2ddd4269973937bde3')

    depends_on('r-callr', type=('build', 'run'))
    depends_on('r-clipr', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rmarkdown', type=('build', 'run'))
    depends_on('r-whisker', type=('build', 'run'))
