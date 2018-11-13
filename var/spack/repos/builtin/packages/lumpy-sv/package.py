# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LumpySv(MakefilePackage):
    """A probabilistic framework for structural variant discovery."""

    homepage = "https://github.com/arq5x/lumpy-sv"
    url      = "https://github.com/arq5x/lumpy-sv/archive/0.2.13.tar.gz"

    version('0.2.13', '36929d29fc3a171d3abbe1d93f9f3b50')

    depends_on('htslib')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('export CXX .*', '')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
