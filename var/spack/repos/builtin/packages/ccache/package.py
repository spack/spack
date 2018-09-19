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


class Ccache(AutotoolsPackage):
    """ccache is a compiler cache. It speeds up recompilation by caching
    previous compilations and detecting when the same compilation is being done
    again."""

    homepage = "https://ccache.samba.org/"
    url      = "https://www.samba.org/ftp/ccache/ccache-3.3.4.tar.gz"

    version('3.3.4', '61326f1edac7cd211a7018458dfe2d86')
    version('3.3.3', 'ea1f95303749b9ac136c617d1b333eef')
    version('3.3.2', 'b966d56603e1fad2bac22930e5f01830')
    version('3.3.1', '7102ef024cff09d353b3f4c48379b40b')
    version('3.3', 'b7ac8fdd556f93831618483325fbb1ef')
    version('3.2.9', '8f3f6e15e75a0e6020166927d41bd0b3')

    depends_on('gperf')
    depends_on('libxslt')
    depends_on('zlib')
