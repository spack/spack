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


class RBiostrings(RPackage):
    """Memory efficient string containers, string matching algorithms, and
       other utilities, for fast manipulation of large biological sequences
       or sets of sequences."""

    homepage = "https://bioconductor.org/packages/Biostrings/"
    git      = "https://git.bioconductor.org/packages/Biostrings.git"

    version('2.48.0', commit='aa3599a7d259d658014d087b86d71ab1deb5f12b')
    version('2.44.2', commit='e4a2b320fb21c5cab3ece7b3c6fecaedfb1e5200')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.6:', when='@2.48.0', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@2.48.0', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.24:', when='@2.48.0', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-xvector@0.19.8:', when='@2.48.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.44.2', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.48.0', type=('build', 'run'))
