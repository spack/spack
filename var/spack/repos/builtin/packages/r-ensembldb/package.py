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


class REnsembldb(RPackage):
    """The package provides functions to create and use transcript centric
       annotation databases/packages. The annotation for the databases are
       directly fetched from Ensembl using their Perl API. The functionality
       and data is similar to that of the TxDb packages from the
       GenomicFeatures package, but, in addition to retrieve all
       gene/transcript models and annotations from the database, the ensembldb
       package provides also a filter framework allowing to retrieve
       annotations for specific entries like genes encoded on a chromosome
       region or transcript models of lincRNA genes."""

    homepage = "https://bioconductor.org/packages/ensembldb/"
    git      = "https://git.bioconductor.org/packages/ensembldb.git"

    version('2.0.4', commit='514623d71e3cca7a4e547adb579b5a958702ef86')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-annotationfilter', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-annotationhub', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', type=('build', 'run'))
