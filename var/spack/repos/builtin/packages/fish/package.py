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


class Fish(AutotoolsPackage):
    """fish is a smart and user-friendly command line shell for OS X, Linux, and
    the rest of the family.
    """

    homepage = "https://fishshell.com/"
    url      = "https://github.com/fish-shell/fish-shell/releases/download/2.7.1/fish-2.7.1.tar.gz"
    list_url = "https://fishshell.com/"

    depends_on('ncurses')

    version('2.7.1', 'e42bb19c7586356905a58578190be792df960fa81de35effb1ca5a5a981f0c5a')
    version('2.7.0', '3a76b7cae92f9f88863c35c832d2427fb66082f98e92a02203dc900b8fa87bcb')
    version('2.2.0', 'a76339fd14ce2ec229283c53e805faac48c3e99d9e3ede9d82c0554acfc7b77a')
