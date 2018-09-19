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


class RPsych(RPackage):
    """A general purpose toolbox for personality, psychometric theory and
       experimental psychology. Functions are primarily for multivariate
       analysis and scale construction using factor analysis, principal
       component analysis, cluster analysis and reliability analysis, although
       others provide basic descriptive statistics. Item Response Theory is
       done using factor analysis of tetrachoric and polychoric correlations.
       Functions for analyzing data at multiple levels include within and
       between group statistics, including correlations and factor analysis.
       Functions for simulating and testing particular item and test structures
       are included. Several functions serve as a useful front end for
       structural equation modeling. Graphical displays of path diagrams,
       factor analysis and structural equation models are created using basic
       graphics. Some of the functions are written to support a book on
       psychometric theory as well as publications in personality research.
       For more information, see the <http://personality-project.org/r> web
       page."""

    homepage = "http://personality-project.org/r/psych"
    url      = "https://cran.r-project.org/src/contrib/psych_1.7.8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/psych"

    version('1.7.8', 'db37f2f85ff5470ee40bbc0a58ebe22b')

    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-foreign', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
