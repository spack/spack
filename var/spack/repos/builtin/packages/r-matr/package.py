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


class RMatr(RPackage):
    """Package matR (Metagenomics Analysis Tools for R) is an analysis
    client for the MG-RAST metagenome annotation engine, part of the US
    Department of Energy (DOE) Systems Biology Knowledge Base (KBase).
    Customized analysis and visualization tools securely access remote
    data and metadata within the popular open source R language and
    environment for statistical computing."""

    homepage = "https://github.com/MG-RAST/matR"
    url      = "https://cran.r-project.org/src/contrib/Archive/matR/matR_0.9.tar.gz"

    version('0.9', 'e2be8734009f5c5b9c1f6b677a77220a')

    depends_on('r-mgraster', type=('build', 'run'))
    depends_on('r-biom-utils', type=('build', 'run'))
