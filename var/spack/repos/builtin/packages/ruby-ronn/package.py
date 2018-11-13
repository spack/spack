# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RubyRonn(Package):
    """Ronn builds manuals. It converts simple, human readable textfiles to
    roff for terminal display, and also to HTML for the web."""

    homepage = "https://rubygems.org/gems/ronn"
    url      = "https://github.com/rtomayko/ronn/archive/0.7.3.tar.gz"

    version('0.7.3', '90cdedb42920c8c2a74e2d177e9535b6')
    version('0.7.0', '34ad78510a75e46904629631f5335e06')

    extends('ruby')

    def install(self, spec, prefix):
        gem('build', 'ronn.gemspec')
        gem('install', 'ronn-{0}.gem'.format(self.version))
