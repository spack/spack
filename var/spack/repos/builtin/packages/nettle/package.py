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


class Nettle(AutotoolsPackage):
    """The Nettle package contains the low-level cryptographic library
    that is designed to fit easily in many contexts."""

    homepage = "https://www.lysator.liu.se/~nisse/nettle/"
    url      = "http://ftp.gnu.org/gnu/nettle/nettle-2.7.1.tar.gz"

    version('3.2', 'afb15b4764ebf1b4e6d06c62bd4d29e4')
    version('2.7', '2caa1bd667c35db71becb93c5d89737f')

    depends_on('gmp')
    depends_on('m4', type='build')
