# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Asciidoctor(Package):
    """Modern asciidoc tool based on ruby"""

    homepage = "https://asciidoctor.org/"
    url      = "https://rubygems.org/downloads/asciidoctor-1.5.8.gem"

    version('1.5.8', '5f55200cab8d1cfcf561e66d3f477159', expand=False)

    extends('ruby')

    def install(self, spec, prefix):
        gem('install', 'asciidoctor-{0}.gem'.format(self.version))
