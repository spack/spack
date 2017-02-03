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


class Yasm(AutotoolsPackage):
    """Yasm is a complete rewrite of the NASM-2.11.06 assembler. It
       supports the x86 and AMD64 instruction sets, accepts NASM and
       GAS assembler syntaxes and outputs binary, ELF32 and ELF64
       object formats."""
    homepage = "http://yasm.tortall.net"
    url      = "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz"

    version('1.3.0', 'fc9e586751ff789b34b1f21d572d96af')
