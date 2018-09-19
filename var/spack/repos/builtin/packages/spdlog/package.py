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


class Spdlog(CMakePackage):
    """Very fast, header only, C++ logging library"""

    homepage = "https://github.com/gabime/spdlog"
    url = "https://github.com/gabime/spdlog/archive/v0.9.0.tar.gz"

    version('0.11.0', '08232203f18a6f9ff47e083cc7a141a050805d3b')
    version('0.10.0', '57b471ef97a23cc29c38b62e00e89a411a87ea7f')
    version('0.9.0', 'dda741ef8e12d57d91f778d85e95a27d84a82ac4')
