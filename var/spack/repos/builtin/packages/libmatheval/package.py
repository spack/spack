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


class Libmatheval(AutotoolsPackage):
    """GNU libmatheval is a library (callable from C and Fortran) to parse
    and evaluate symbolic expressions input as text. It supports expressions
    in any number of variables of arbitrary names, decimal and symbolic
    constants, basic unary and binary operators, and elementary mathematical
    functions. In addition to parsing and evaluation, libmatheval can also
    compute symbolic derivatives and output expressions to strings."""

    homepage = "https://www.gnu.org/software/libmatheval/"
    url      = "https://ftpmirror.gnu.org/libmatheval/libmatheval-1.1.11.tar.gz"

    version('1.1.11', '595420ea60f6ddd75623847f46ca45c4')

    # Only needed for unit tests, but configure crashes without it
    depends_on('guile', type='build')

    # guile 2.0 provides a deprecated interface for the unit test using guile
    patch('guile-2.0.patch', when='^guile@2.0')

    # guile 2.2 does not support deprecated functions any longer
    # the patch skips the unit tests
    patch('guile-2.2.patch', when='^guile@2.2:')
