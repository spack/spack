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


class RNloptr(RPackage):
    """nloptr is an R interface to NLopt. NLopt is a free/open-source
    library for nonlinear optimization, providing a common interface
    for a number of different free optimization routines available
    online as well as original implementations of various other
    algorithms. See http://ab-initio.mit.edu/wiki/index.php/NLopt
    _Introduction for more information on the available algorithms.
    During installation on Unix the NLopt code is downloaded and
    compiled from the NLopt website."""

    homepage = "https://cran.r-project.org/package=nloptr"
    url      = "https://cran.rstudio.com/src/contrib/nloptr_1.0.4.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/nloptr"

    version('1.0.4', 'f2775dfb4f7f5552d46937a04c062b0d')

    depends_on('r-testthat', type=('build', 'run'))
