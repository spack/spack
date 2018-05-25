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


class Denovogear(CMakePackage):
    """DeNovoGear is a software package to detect de novo mutations using
    next-generation sequencing data. It supports the analysis of many
    differential experimental designs and uses advanced statistical models
    to reduce the false positve rate."""

    homepage = "https://github.com/denovogear/denovogear"
    url      = "https://github.com/denovogear/denovogear/archive/v1.1.1.tar.gz"

    version('1.1.1', 'da30e46851c3a774653e57f98fe62e5f')
    version('1.1.0', '7d441d56462efb7ff5d3a6f6bddfd8b9')

    depends_on('cmake@3.1:', type=('build'))
    depends_on('boost@1.47:1.60', type=('build'))
    depends_on('htslib@1.2:', type=('build'))
    depends_on('eigen', type=('build'))
