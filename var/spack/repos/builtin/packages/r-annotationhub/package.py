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


class RAnnotationhub(RPackage):
    """This package provides a client for the Bioconductor AnnotationHub web
       resource. The AnnotationHub web resource provides a central location
       where genomic files (e.g., VCF, bed, wig) and other resources from
       standard locations (e.g., UCSC, Ensembl) can be discovered. The
       resource includes metadata about each resource, e.g., a textual
       description, tags, and date of modification. The client creates and
       manages a local cache of files retrieved by the user, helping with
       quick and reproducible access."""

    homepage = "https://bioconductor.org/packages/AnnotationHub/"
    git      = "https://git.bioconductor.org/packages/AnnotationHub.git"

    version('2.8.3', commit='8aa9c64262a8d708d2bf1c82f82dfc3d7d4ccc0c')

    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-interactivedisplaybase', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.8.3')
