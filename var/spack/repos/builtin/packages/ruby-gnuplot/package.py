# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RubyGnuplot(Package):
    """Utility library to aid in interacting with gnuplot from ruby"""

    homepage = "https://rubygems.org/gems/gnuplot/versions/2.6.2"
    url      = "https://rubygems.org/downloads/gnuplot-2.6.2.gem"

    version('2.6.2', sha256='d2c28d4a55867ef6f0a5725ce157581917b4d27417bc3767c7c643a828416bb3', expand=False)

    depends_on('gnuplot+X')

    extends('ruby')

    def install(self, spec, prefix):
        gem('install', 'gnuplot-{0}.gem'.format(self.version))
