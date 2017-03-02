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


class Atompaw(Package):
    """A Projector Augmented Wave (PAW) code for generating
    atom-centered functions.

    Official website: http://pwpaw.wfu.edu

    User's guide: ~/doc/atompaw-usersguide.pdf
    """
    homepage = "http://users.wfu.edu/natalie/papers/pwpaw/man.html"
    url = "http://users.wfu.edu/natalie/papers/pwpaw/atompaw-4.0.0.13.tar.gz"

    version('4.0.0.13', 'af4a042380356f6780183c4b325aad1d')
    version('3.1.0.3', 'c996a277e11707887177f47bbb229aa6')

    depends_on("lapack")
    depends_on("blas")

    # pin libxc version
    depends_on("libxc@2.2.1")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]

        linalg = spec['lapack'].libs + spec['blas'].libs
        options.extend([
            "--with-linalg-libs=%s" % linalg.ld_flags,
            "--enable-libxc",
            "--with-libxc-incs=-I%s" % spec["libxc"].prefix.include,
            "--with-libxc-libs=-L%s -lxcf90 -lxc" % spec["libxc"].prefix.lib,
        ])

        configure(*options)
        make(parallel=False)  # parallel build fails
        make("check")
        make("install")
