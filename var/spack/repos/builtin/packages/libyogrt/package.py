##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Libyogrt(AutotoolsPackage):
    """Your One Get Remaining Time Library."""

    homepage = "https://github.com/LLNL/libyogrt"
    url      = "https://github.com/LLNL/libyogrt/archive/1.20-6.tar.gz"

    version('1.21',   '00c282f29109725d272079e49edb4737',
            url='https://github.com/LLNL/libyogrt/releases/download/1.21/libyogrt-1.21.tar.gz')
    version('1.20-6', '478f27512842cc5f2b74a0c22b851f60')
    version('1.20-5', 'd0fa6526fcd1f56ddb3d93f602ec72f7')
    version('1.20-4', '092bea10de22c505ce92aa07001decbb')
    version('1.20-3', 'd0507717009a5f8e2009e3b63594738f')
    version('1.20-2', '780bda03268324f6b5f72631fff6e6cb')

    # TODO: only want this variant available for v1.21 and greater, how?
    # @when("libyogrt@1.21:")
    variant("lsf", default=False,
            description="Build backend for LSF")

    def configure_args(self):
        spec = self.spec
        args = []

        # the lsf variant is only valid for v1.21 and later
        if "+lsf" in spec and "libyogrt@1.21:" in spec:
            args.append("--with-lsf=/opt/ibm/spectrumcomputing/lsf/10.1")

        return args
