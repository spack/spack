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


class RSmoof(RPackage):
    """Provides generators for a high number of both single- and
       multi- objective test functions which are frequently used for the
       benchmarking of (numerical) optimization algorithms. Moreover, it offers
       a set of convenient functions to generate, plot and work with objective
       functions."""

    homepage = "http://github.com/jakobbossek/smoof"
    url      = "https://cran.r-project.org/src/contrib/smoof_1.5.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/smoof"

    version('1.5.1', 'c3e3b5dafed34608f933ae255cf49054')
    version('1.5', 'b371bde2724eade5a6d4d808fa3ad269')

    depends_on('r-paramhelpers@1.8:', type=('build', 'run'))
    depends_on('r-bbmisc@1.6:', type=('build', 'run'))
    depends_on('r-checkmate@1.1:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.1:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-plot3d', type=('build', 'run'))
    depends_on('r-plotly', type=('build', 'run'))
    depends_on('r-mco', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rjsonio', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
