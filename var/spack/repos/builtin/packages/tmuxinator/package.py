# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tmuxinator(Package):
    """A session configuration creator and manager for tmux"""

    homepage = "https://github.com/tmuxinator/tmuxinator"
    git      = "https://github.com/tmuxinator/tmuxinator.git"

    version('0.6.11', tag='v0.6.11')

    extends('ruby')

    def install(self, spec, prefix):
        gem('build', 'tmuxinator.gemspec')
        gem('install', 'tmuxinator-{0}.gem'.format(self.version))
