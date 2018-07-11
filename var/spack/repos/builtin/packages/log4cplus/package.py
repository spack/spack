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


class Log4cplus(CMakePackage):
    """log4cplus is a simple to use C++ logging API
    providing thread-safe, flexible, and arbitrarily
    granular control over log management and configuration."""

    homepage = "https://sourceforge.net/projects/log4cplus/"
    url      = "https://download.sourceforge.net/project/log4cplus/log4cplus-stable/2.0.1/log4cplus-2.0.1.tar.bz2"

    version('2.0.1', 'ec01c03241ebd31127a44d1880830d8f')
    version('1.2.1', 'e4e6c38b065b70b5d6efc238a5106bc9')
    version('1.2.0', 'e250f0f431c0723f8b625323e7b6465d')
