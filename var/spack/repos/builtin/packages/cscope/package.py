##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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


class Cscope(AutotoolsPackage):
    """Cscope is a developer's tool for browsing source code."""

    homepage = "http://cscope.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/cscope/cscope/15.8b/cscope-15.8b.tar.gz"

    version('15.8b', '8f9409a238ee313a96f9f87fe0f3b176')

    variant('flex', default=False, description="Builds with flex")

    depends_on('flex', when='+flex')

    def configure_args(self):
        args = []
        if '+flex' in self.spec:
            args.append('--with-flex')
        return args
