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


class Gmime(AutotoolsPackage):
    """GMime is a C/C++ library which may be used for the creation and
    parsing of messages using the Multipurpose Internet Mail Extension (MIME).
    """

    homepage = "http://spruce.sourceforge.net/gmime/"
    url      = "https://download.gnome.org/sources/gmime/2.6/gmime-2.6.23.tar.xz"

    version('2.6.23', '247072236d84bd0fbbff299d69bdf333')

    depends_on('glib@2.18.0:')
    depends_on('libgpg-error')
