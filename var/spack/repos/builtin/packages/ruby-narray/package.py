# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RubyNarray(Package):
    """Numo::NArray is an Numerical N-dimensional Array class for fast
       processing and easy manipulation of multi-dimensional numerical data,
       similar to numpy.ndaray."""

    homepage = "https://rubygems.org/gems/narray"
    git      = "https://github.com/ruby-numo/narray.git"

    version('0.9.0.9', commit='9cadbbccf1e01b6d1bc143c19d598cad1c420869')

    extends('ruby')

    def install(self, spec, prefix):
        gem('build', 'numo-narray.gemspec')
        gem('install', 'numo-narray-{0}.gem'.format(self.version))
