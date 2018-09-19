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


class Bedtools2(Package):
    """Collectively, the bedtools utilities are a swiss-army knife of
       tools for a wide-range of genomics analysis tasks. The most
       widely-used tools enable genome arithmetic: that is, set theory
       on the genome."""

    homepage = "https://github.com/arq5x/bedtools2"
    url      = "https://github.com/arq5x/bedtools2/archive/v2.26.0.tar.gz"

    version('2.27.1', '8e0afcab95a824e42a6e99c5436a8438')
    version('2.27.0', '052f22eb214ef2e7e7981b3c01167302')
    version('2.26.0', '52227e7efa6627f0f95d7d734973233d')
    version('2.25.0', '534fb4a7bf0d0c3f05be52a0160d8e3d')
    version('2.23.0', '4fa3671b3a3891eefd969ad3509222e3')

    depends_on('zlib')

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")
