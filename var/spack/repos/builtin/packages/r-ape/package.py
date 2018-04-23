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


class RApe(RPackage):
    """Functions for reading, writing, plotting, and manipulating phylogenetic
    trees, analyses of comparative data in a phylogenetic framework, ancestral
    character analyses, analyses of diversification and macroevolution,
    computing distances from DNA sequences, reading and writing nucleotide
    sequences as well as importing from BioConductor, and several tools such
    as Mantel's test, generalized skyline plots, graphical exploration of
    phylogenetic data (alex, trex, kronoviz), estimation of absolute
    evolutionary rates and clock-like trees using mean path lengths and
    penalized likelihood, dating trees with non-contemporaneous sequences,
    translating DNA into AA sequences, and assessing sequence alignments.
    Phylogeny estimation can be done with the NJ, BIONJ, ME, MVR, SDM, and
    triangle methods, and several methods handling incomplete distance
    matrices (NJ*, BIONJ*, MVR*, and the corresponding triangle method). Some
    functions call external applications (PhyML, Clustal, T-Coffee, Muscle)
    whose results are returned into R."""

    homepage = "http://ape-package.ird.fr/"
    url      = "https://cran.r-project.org/src/contrib/ape_4.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ape"

    version('5.0', '82fd2786a502f070ca020797f7b19fa4')
    version('4.1', 'a9ed416d6d172d4b9682556cf692d7c2')

    depends_on('r@3.2:')
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
