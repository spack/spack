# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glpk(AutotoolsPackage):
    """The GLPK (GNU Linear Programming Kit) package is intended for solving
    large-scale linear programming (LP), mixed integer programming
    (MIP), and other related problems. It is a set of routines written
    in ANSI C and organized in the form of a callable library.
    """

    homepage = "https://www.gnu.org/software/glpk"
    url      = "https://ftpmirror.gnu.org/glpk/glpk-4.65.tar.gz"

    version('4.65', '470a984a8b1c0e027bdb6d5859063fe8')
    version('4.61', '3ce3e224a8b6e75a1a0b378445830f21')
    version('4.57', '237531a54f73155842f8defe51aedb0f')

    variant(
        'gmp', default=False, description='Activates support for GMP library'
    )

    depends_on('gmp', when='+gmp')

    def configure_args(self):

        options = []

        if '+gmp' in self.spec:
            options.append('--with-gmp')

        return options
