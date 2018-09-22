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

    version('1.1.0',  sha256='3dbcbfd8c07e25f5e0d662b194d3a7772ef214358c49ada23c044c4747ce8b19')
    version('1.0.0',  sha256='90d5365121bcd2c41ce94dfe6a460e89507a2dfef6133fe5fad5bb35ac4ef0a1')
    version('0.17.0', sha256='94f74fd1b3344733d1db3de2ec22e6cbeb769f93a8baa0d4a22b1f62dc7369f8')
    version('0.16.3', sha256='b88d7be261d9089c817fc8cee6c000d69f349b357828e4c7f66985bc5d5360b8')
    version('0.16.2', sha256='2081e5df5e87402398847431e16b87c71dd5c4d632314bb976ace8161f4d32de')
    version('0.16.1', sha256='733260e1fbdcf1b3dc307fc585e4476240026de8be28eb905731d2ab0942deae')
    version('0.16.0', sha256='9e64e3b10c2a3c54dfff63aa056057cf1db8a5fd506b3d9cf77207511820baac')
    version('0.14.0', sha256='eb5beb4e53f4bfff5b32eb4db8588484bdc15a17b90eeefef3a9fc74fec1d83d')
    version('0.13.0', sha256='d798a6ca19165f0a18a43938859359269f5a07fd8e0eb83ab8674739c9e8f361')
    version('0.12.0', sha256='5cfd6a0b3182a88e1eb35bcb65a7ef9035140d7c73b16ba6095939dbf07325b9')
    version('0.11.0', '08232203f18a6f9ff47e083cc7a141a050805d3b')
    version('0.10.0', '57b471ef97a23cc29c38b62e00e89a411a87ea7f')
    version('0.9.0', 'dda741ef8e12d57d91f778d85e95a27d84a82ac4')
