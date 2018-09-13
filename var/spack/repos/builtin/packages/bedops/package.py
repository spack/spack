##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Bedops(MakefilePackage):
    """BEDOPS is an open-source command-line toolkit that performs highly
    efficient and scalable Boolean and other set operations, statistical
    calculations, archiving, conversion and other management of genomic data of
    arbitrary scale."""

    homepage = "https://bedops.readthedocs.io"
    url      = "https://github.com/bedops/bedops/archive/v2.4.30.tar.gz"

    version('2.4.35', 'b425b3e05fd4cd1024ef4dd8bf04b4e5')
    version('2.4.34', 'fc467d96134a0efe8b134e638af87a1a')
    version('2.4.30', '4e5d9f7b7e5432b28aef8d17a22cffab')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make('install', "BINDIR=%s" % prefix.bin)
