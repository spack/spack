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


class Libepoxy(AutotoolsPackage):
    """Epoxy is a library for handling OpenGL function pointer management for
    you."""
    homepage = "https://github.com/anholt/libepoxy"
    url      = "https://github.com/anholt/libepoxy/releases/download/1.4.3/libepoxy-1.4.3.tar.xz"
    list_url = "https://github.com/anholt/libepoxy/releases"

    version('1.4.3', 'af4c3ce0fb1143bdc4e43f85695a9bed')
    version('1.3.1', '96f6620a9b005a503e7b44b0b528287d')

    depends_on('meson')
    depends_on('mesa')
