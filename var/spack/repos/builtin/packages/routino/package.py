# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Routino(MakefilePackage):
    """Routino is an application for finding a route between two points using
    the dataset of topographical information collected by
    http://www.OpenStreetMap.org."""

    homepage = "https://www.routino.org"
    url      = "https://www.routino.org/download/routino-3.2.tgz"

    version('3.3.3', sha256='abd82b77c314048f45030f7219887ca241b46d40641db6ccb462202b97a047f5')
    version('3.3.2', sha256='4b7174d76955e058986d343635e0a184385f2756fa4ffc02eb5e2399921e9db1')
    version('3.3.1', sha256='a954565ab60a5abebc47e8c6e8b496f972e8dd781810fa5548b6d7a9e3e5e135')
    version('3.3',   sha256='f1095fa05438e9a85e6fa7d6fb334f681b96e7c6033abf1164d4de2170ea03bb')
    version('3.2', sha256='e2a431eaffbafab630835966d342e4ae25d5edb94c8ed419200e1ffb50bc7552')

    depends_on('zlib')
    depends_on('bzip2')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile.conf')
        makefile.filter('prefix=.*', 'prefix={0}'.format(prefix))
