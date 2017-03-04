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


class XorgSgmlDoctools(AutotoolsPackage):
    """This package provides a common set of SGML entities and XML/CSS style
    sheets used in building/formatting the documentation provided in other
    X.Org packages."""

    homepage = "http://cgit.freedesktop.org/xorg/doc/xorg-sgml-doctools"
    url      = "https://www.x.org/archive/individual/doc/xorg-sgml-doctools-1.11.tar.gz"

    version('1.11', '51cf4c6b476e2b98a068fea6975b9b21')

    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
