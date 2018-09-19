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


class Libtermkey(Package):
    """Easy keyboard entry processing for terminal programs"""
    homepage = "http://www.leonerd.org.uk/code/libtermkey/"
    url      = "http://www.leonerd.org.uk/code/libtermkey/libtermkey-0.18.tar.gz"

    version('0.18', '3be2e3e5a851a49cc5e8567ac108b520')
    version('0.17', '20edb99e0d95ec1690fe90e6a555ae6d')
    version('0.16', '7a24b675aaeb142d30db28e7554987d4')
    version('0.15b', '27689756e6c86c56ae454f2ac259bc3d')
    version('0.14', 'e08ce30f440f9715c459060e0e048978')

    depends_on('libtool', type='build')
    depends_on('ncurses')

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
