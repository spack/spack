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

class Pocl(Package):
    """Portable Computing Language"""
    homepage = "http://portablecl.org"
    url      = "http://portablecl.org/downloads/pocl-0.13.tar.gz"

    version('0.13', '344480864d4269f2f63f1509395898bd')
    version('0.12', 'e197ba3aa01a35f40581c48e053330dd')
    version('0.11', '9be0640cde2983062c47393d9e8e8fe7')
    version('0.10', '0096be4f595c7b5cbfa42430c8b3af6a')
    version('0.9' , 'f95f4a9e7870854c60be2d2269c3ebec')

    depends_on("llvm +clang")
    depends_on("libtool")
    depends_on("hwloc")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--disable-icd")
        make()
        make("install")
