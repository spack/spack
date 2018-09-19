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


class RDelayedarray(RPackage):
    """Wrapping an array-like object (typically an on-disk object) in a
       DelayedArray object allows one to perform common array operations on it
       without loading the object in memory. In order to reduce memory usage
       and optimize performance, operations on the object are either delayed
       or executed using a block processing mechanism. Note that this also
       works on in-memory array-like objects like DataFrame objects (typically
       with Rle columns), Matrix objects, and ordinary arrays and data frames.
       Wrapping an array-like object (typically an on-disk object) in a
       DelayedArray object allows one to perform common array operations on it
       without loading the object in memory. In order to reduce memory usage
       and optimize performance, operations on the object are either delayed
       or executed using a block processing mechanism. Note that this also
       works on in-memory array-like objects like DataFrame objects (typically
       with Rle columns), Matrix objects, and ordinary arrays and data
       frames."""

    homepage = "https://bioconductor.org/packages/DelayedArray/"
    git      = "https://git.bioconductor.org/packages/DelayedArray.git"

    version('0.6.5', commit='7d1cb6477cb024c38bf1ee0c9155e010249ed94e')
    version('0.4.1', commit='ffe932ef8c255614340e4856fc6e0b44128a27a1')
    version('0.2.7', commit='909c2ce1665ebae2543172ead50abbe10bd42bc4')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.25.1:', when='@0.6.5', type=('build', 'run'))
    depends_on('r-s4vectors@0.14.3:', when='@0.2.7', type=('build', 'run'))
    depends_on('r-s4vectors@0.15.3:', when='@0.4.1', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.43:', when='@0.6.5', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.11.17:', when='@0.4.1:', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@0.2.7', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@0.6.5', type=('build', 'run'))
