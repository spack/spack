# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Kakoune(MakefilePackage):
    """mawww's experiment for a better code editor."""

    homepage = "https://www.kakoune.org"
    url      = "https://github.com/mawww/kakoune/releases/download/v2021.11.08/kakoune-2021.11.08.tar.bz2"

    maintainers = ['Bambi']

    version('2021.11.08', sha256='aa30889d9da11331a243a8f40fe4f6a8619321b19217debac8f565e06eddb5f4')

    depends_on('ncurses')

    conflicts('%gcc@:8', when='@2021.11.08', msg='GCC version must be at least 9.0!')

    build_targets = ['all', 'man']

    def edit(self, spec, prefix):
        env['PREFIX'] = prefix
