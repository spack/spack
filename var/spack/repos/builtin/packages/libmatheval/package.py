# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    depends_on('flex')

    # guile 2.0 provides a deprecated interface for the unit test using guile
    patch('guile-2.0.patch', when='^guile@2.0')

    # guile 2.2 does not support deprecated functions any longer
    # the patch skips the unit tests
    patch('guile-2.2.patch', when='^guile@2.2:')
