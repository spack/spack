# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RubyGnuplot(Package):
    """Utility library to aid in interacting with gnuplot from ruby"""

    homepage = "https://rubygems.org/gems/gnuplot/versions/2.6.2"
    url      = "https://rubygems.org/downloads/gnuplot-2.6.2.gem"

    version('2.6.2', 'ff36a37cf71b9cd6273fcd14bbfd82df', expand=False)

    depends_on('gnuplot+X')

    extends('ruby')

    def install(self, spec, prefix):
        gem('install', 'gnuplot-{0}.gem'.format(self.version))
