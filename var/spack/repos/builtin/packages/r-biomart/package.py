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


class RBiomart(RPackage):
    """In recent years a wealth of biological data has become available in
       public data repositories. Easy access to these valuable data resources
       and firm integration with data analysis is needed for comprehensive
       bioinformatics data analysis. biomaRt provides an interface to a growing
       collection of databases implementing the BioMart software suite
       (http://www.biomart.org). The package enables retrieval of large amounts
       of data in a uniform way without the need to know the underlying
       database schemas or write complex SQL queries. Examples of BioMart
       databases are Ensembl, COSMIC, Uniprot, HGNC, Gramene, Wormbase and
       dbSNP mapped to Ensembl. These major databases give biomaRt users direct
       access to a diverse set of data and enable a wide range of powerful
       online queries from gene annotation to database mining."""

    homepage = "https://bioconductor.org/packages/biomaRt/"
    git      = "https://git.bioconductor.org/packages/biomaRt.git"

    version('2.34.2', commit='a7030915fbc6120cc6812aefdedba423a207459b')
    version('2.32.1', commit='f84d74424fa599f6d08f8db4612ca09914a9087f')

    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-progress', type=('build', 'run'), when='@2.34.2')
    depends_on('r-stringr', type=('build', 'run'), when='@2.34.2')
    depends_on('r-httr', type=('build', 'run'), when='@2.34.2')
    depends_on('r@3.4.0:3.4.9', when='@2.32.1:')
