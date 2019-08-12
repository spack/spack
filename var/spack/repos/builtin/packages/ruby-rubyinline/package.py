# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RubyRubyinline(Package):
    """Inline allows you to write foreign code within your ruby code."""

    homepage = "https://rubygems.org/gems/RubyInline"
    url      = "https://rubygems.org/downloads/RubyInline-3.12.4.gem"

    version('3.12.4', '3058f4c48e62baef811b127f4925ee70', expand=False)

    extends('ruby')

    def install(self, spec, prefix):
        gem('install', 'RubyInline-{0}.gem'.format(self.version))
