##############################################################################
# Copyright (c) 2018, Lawrence Livermore National Security, LLC.
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


class Ragel(AutotoolsPackage):
    """Ragel State Machine Compiler
    Ragel compiles executable finite state machines from regular
    languages. Ragel targets C, C++ and ASM. Ragel state machines can
    not only recognize byte sequences as regular expression machines
    do, but can also execute code at arbitrary points in the
    recognition of a regular language. Code embedding is done using
    inline operators that do not disrupt the regular language syntax.
    """
    homepage = "http://www.colm.net/open-source/ragel"
    git      = "git://colm.net/ragel.git"
    url      = "http://www.colm.net/files/ragel/ragel-6.10.tar.gz"

    version('6.10', '748cae8b50cffe9efcaa5acebc6abf0d')

    depends_on('colm', type='build')
