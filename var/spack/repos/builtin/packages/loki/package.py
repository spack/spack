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


class Loki(MakefilePackage):
    """Loki is a C++ library of designs, containing flexible implementations
    of common design patterns and idioms."""

    homepage = "http://loki-lib.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/loki-lib/Loki/Loki%200.1.7/loki-0.1.7.tar.bz2"

    version('0.1.7', '33a24bcbb99fa2ec8fcbbab65649f3f6')

    variant('shared', default=True, description="Build shared libraries")

    def build(self, spec, prefix):
        if '+shared' in spec:
            make('-C', 'src', 'build-shared')
        else:
            make('-C', 'src', 'build-static')

    def install(self, spec, prefix):
        make('-C', 'include', 'install', 'prefix={0}'.format(prefix))
        if '+shared' in spec:
            make('-C', 'src', 'install-shared', 'prefix={0}'.format(prefix))
        else:
            make('-C', 'src', 'install-static', 'prefix={0}'.format(prefix))
