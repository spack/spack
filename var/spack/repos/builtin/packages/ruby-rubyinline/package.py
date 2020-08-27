# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RubyRubyinline(Package):
    """Inline allows you to write foreign code within your ruby code."""

    homepage = "https://rubygems.org/gems/RubyInline"
    url      = "https://rubygems.org/downloads/RubyInline-3.12.4.gem"

    version('3.12.4', sha256='205bbc14c02d3d55e1b497241ede832ab87f3d981f92f3bda98b75e8144103e0', expand=False)

    extends('ruby')

    def install(self, spec, prefix):
        gem('install', 'RubyInline-{0}.gem'.format(self.version))
