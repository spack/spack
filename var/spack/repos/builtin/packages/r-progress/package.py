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
