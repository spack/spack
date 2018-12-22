# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Blitz(AutotoolsPackage):
    """N-dimensional arrays for C++"""
    homepage = "http://github.com/blitzpp/blitz"
    url = "https://github.com/blitzpp/blitz/archive/1.0.1.tar.gz"

    version('1.0.1', 'fe43e2cf6c9258bc8b369264dd008971')
    version('1.0.0', '971c43e22318bbfe8da016e6ef596234')

    build_targets = ['lib']

    def check(self):
        make('check-testsuite')
        make('check-examples')
