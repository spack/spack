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


class RAnnotationfilter(RPackage):
    """This package provides class and other infrastructure to implement
       filters for manipulating Bioconductor annotation resources. The
       filters will be used by ensembldb, Organism.dplyr, and other
       packages."""

    homepage = "https://bioconductor.org/packages/AnnotationFilter/"
    git      = "https://git.bioconductor.org/packages/AnnotationFilter.git"

    version('1.0.0', commit='a9f79b26defe3021eea60abe16ce1fa379813ec9')

    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.0.0')
