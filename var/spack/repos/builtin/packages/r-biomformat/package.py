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


class RBiomformat(RPackage):
    """This is an R package for interfacing with the BIOM format. This
    package includes basic tools for reading biom-format files, accessing
    and subsetting data tables from a biom object (which is more complex
    than a single table), as well as limited support for writing a
    biom-object back to a biom-format file. The design of this API is
    intended to match the python API and other tools included with the
    biom-format project, but with a decidedly "R flavor" that should be
    familiar to R users. This includes S4 classes and methods, as well
    as extensions of common core functions/methods."""

    homepage = "https://www.bioconductor.org/packages/biomformat/"
    git      = "https://git.bioconductor.org/packages/biomformat.git"

    version('1.4.0', commit='83b4b1883bc56ea93a0a6ca90fc1b18712ef0f1a')

    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rhdf5', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.4.0')
