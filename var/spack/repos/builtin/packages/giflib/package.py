# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Giflib(AutotoolsPackage):
    """The GIFLIB project maintains the giflib service library, which has
    been pulling images out of GIFs since 1989."""

    homepage = "http://giflib.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/giflib/giflib-5.1.4.tar.bz2"

    version('5.1.4', '2c171ced93c0e83bb09e6ccad8e3ba2b')

    patch('bsd-head.patch')

    def check(self):
        make('check', parallel=False)
