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


class RGsubfn(RPackage):
    """gsubfn is like gsub but can take a replacement function or
    certain other objects instead of the replacement string. Matches
    and back references are input to the replacement function and
    replaced by the function output. gsubfn can be used to split
    strings based on content rather than delimiters and for
    quasi-perl-style string interpolation. The package also has
    facilities for translating formulas to functions and allowing
    such formulas in function calls instead of functions. This can
    be used with R functions such as apply, sapply, lapply, optim,
    integrate, xyplot, Filter and any other function that expects
    another function as an input argument or functions like cat or
    sql calls that may involve strings where substitution is
    desirable."""

    homepage = "https://cran.r-project.org/package=gsubfn"
    url      = "https://cran.r-project.org/src/contrib/gsubfn_0.6-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gsubfn"

    version('0.6-6', '94195ff3502706c736d9c593c07252bc')

    depends_on('r-proto', type=('build', 'run'))
