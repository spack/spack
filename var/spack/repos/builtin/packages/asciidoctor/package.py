# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Asciidoctor(Package):
    """Modern asciidoc tool based on ruby"""

    homepage = "https://asciidoctor.org/"
    url      = "https://rubygems.org/downloads/asciidoctor-1.5.8.gem"

    version('1.5.8', sha256='9deaa93eacadda48671e18395b992eafba35d08f25ddbe28d25bb275831a8d62', expand=False)

    extends('ruby')

    def install(self, spec, prefix):
        gem('install', 'asciidoctor-{0}.gem'.format(self.version))
