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


class Gem5(SConsPackage):
    """The gem5 simulator is a modular platform
    for computer-system architecture research,
    encompassing system-level architecture
    as well as processor microarchitecture."""

    homepage = "http://www.gem5.org"
    url      = "https://github.com/gem5/gem5/archive/stable_2015_09_03.tar.gz"

    version('2015_09_03', 'a7e926d1a64b302b38a10d6bf57bfb2d')

    depends_on('m4', type='build')
    depends_on('swig', type='build')
    depends_on('python')
    depends_on('zlib')

    # def build_args(self, spec, prefix):
    #     # FIXME: Add arguments to pass to build.
    #     # FIXME: If not needed delete this function
    #     args = []
    #     return args
