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


class RRhdf5(RPackage):
    """This R/Bioconductor package provides an interface between HDF5
    and R. HDF5's main features are the ability to store and access very
    large and/or complex datasets and a wide variety of metadata on mass
    storage (disk) through a completely portable file format. The rhdf5
    package is thus suited for the exchange of large and/or complex
    datasets between R and other software package, and for letting R
    applications work on datasets that are larger than the available RAM."""

    homepage = "https://www.bioconductor.org/packages/rhdf5/"
    git      = "https://git.bioconductor.org/packages/rhdf5.git"

    version('2.20.0', commit='37b5165325062728bbec9167f89f5f4b794f30bc')

    depends_on('r@3.4.0:3.4.9', when='@2.20.0')
    depends_on('r-zlibbioc', type=('build', 'run'))
