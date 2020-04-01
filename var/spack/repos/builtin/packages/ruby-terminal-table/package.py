# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RubyTerminalTable(Package):
    """Simple, feature rich ascii table generation library"""

    homepage = "https://rubygems.org/gems/terminal-table"
    url      = "https://rubygems.org/downloads/terminal-table-1.8.0.gem"

    version('1.8.0', sha256='13371f069af18e9baa4e44d404a4ada9301899ce0530c237ac1a96c19f652294', expand=False)

    extends('ruby')

    def install(self, spec, prefix):
        gem('install', 'terminal-table-{0}.gem'.format(self.version))
