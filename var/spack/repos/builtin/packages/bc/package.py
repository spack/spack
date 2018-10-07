# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bc(AutotoolsPackage):
    """bc is an arbitrary precision numeric processing language. Syntax is
    similar to C, but differs in many substantial areas. It supports
    interactive execution of statements."""

    homepage = "https://www.gnu.org/software/bc"
    url      = "https://ftpmirror.gnu.org/bc/bc-1.07.tar.gz"

    version('1.07', 'e91638a947beadabf4d7770bdbb3d512')

    depends_on('ed', type='build')
    depends_on('texinfo', type='build')

    parallel = False
