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


class UtilMacros(AutotoolsPackage):
    """This is a set of autoconf macros used by the configure.ac scripts in
    other Xorg modular packages, and is needed to generate new versions
    of their configure scripts with autoconf."""

    homepage = "http://cgit.freedesktop.org/xorg/util/macros/"
    url = "https://www.x.org/archive/individual/util/util-macros-1.19.1.tar.bz2"

    version('1.19.1', '6e76e546a4e580f15cebaf8019ef1625')
    version('1.19.0', '1cf984125e75f8204938d998a8b6c1e1')
