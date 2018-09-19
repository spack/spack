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


class Dejagnu(AutotoolsPackage):
    """DejaGnu is a framework for testing other programs. Its purpose
    is to provide a single front end for all tests."""

    homepage = "https://www.gnu.org/software/dejagnu/"
    url      = "https://ftpmirror.gnu.org/dejagnu/dejagnu-1.6.tar.gz"

    version('1.6',   '1fdc2eb0d592c4f89d82d24dfdf02f0b')
    version('1.4.4', '053f18fd5d00873de365413cab17a666')

    depends_on('expect')
    depends_on('tcl@8.5:')

    # DejaGnu 1.4.4 cannot be built in parallel
    # `make check` also fails but this can be ignored
    parallel = False
