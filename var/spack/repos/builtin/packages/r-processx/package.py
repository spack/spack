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


class RProcessx(RPackage):
    """Tools to run system processes in the background"""

    homepage = "https://github.com/r-lib/processx"
    url      = "https://cran.r-project.org/src/contrib/processx_3.2.0.tar.gz"
    list_url      = "https://cran.r-project.org/src/contrib/Archive/processx/processx_3.1.0.tar.gz"

    version('3.2.0', sha256='c4ba602fcbdc032ae9d94701b3e6b83a2dab1b53d0b4f9937b07a84eae22fddf')
    version('3.1.0',   sha256='11ac120ab4e4aa0e99c9b2eda87d07bc683bab735f1761e95e5ddacd311b5972')
    version('3.0.3',   sha256='53781dba3c538605a02e28b3b577e7de79e2064bfc502025f7ec0e5945e302bf')
    version('2.0.0.1', sha256='8f61b2952d0f2d13c74465bfba174ce11eee559475c2f7b9be6bcb9e2e1d827b')
    version('2.0.0',   sha256='8325b56a60a276909228756281523cda9256bc754c5f3ca03b41c5c17cc398ad')

    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-ps', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-utils', type=('build', 'run'))
