# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glimmer(MakefilePackage):
    """Glimmer is a system for finding genes in microbial DNA, especially the
    genomes of bacteria, archaea, and viruses."""

    homepage = "https://ccb.jhu.edu/software/glimmer"

    version('3.02b', '344d012ae12596de905866fe9eb7f16c')

    build_directory = 'src'

    def url_for_version(self, version):
        url = "https://ccb.jhu.edu/software/glimmer/glimmer{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
