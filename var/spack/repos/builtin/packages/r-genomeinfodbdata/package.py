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


class RGenomeinfodbdata(RPackage):
    """for mapping between NCBI taxonomy ID and species. Used by functions
       in the GenomeInfoDb package."""

    homepage = "https://bioconductor.org/packages/GenomeInfoDbData/"
    url      = "https://bioconductor.org/packages/3.5/data/annotation/src/contrib/GenomeInfoDbData_0.99.0.tar.gz"

    version('1.1.0', '6efdca22839c90d455843bdab7c0ecb5d48e3b6c2f7b4882d3210a6bbad4304c',
            url='https://bioconductor.org/packages/release/data/annotation/src/contrib/GenomeInfoDbData_1.1.0.tar.gz')
    version('0.99.0', '85977b51061dd02a90153db887040d05')
    depends_on('r@3.4.0:3.4.9', when='@0.99.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.1.0', type=('build', 'run'))
