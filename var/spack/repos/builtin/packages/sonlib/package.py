# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Sonlib(MakefilePackage):
    """sonLib is a compact C/Python library for
    sequence analysis in bioinformatics."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/benedictpaten/sonLib"
    url      = "https://github.com/ComparativeGenomicsToolkit/sonLib"
    git      = "https://github.com/ComparativeGenomicsToolkit/sonLib.git"

    # This is sonlib as needed by the hal package
    #
    # If you need to use sonlib then you want py-sonlib

    version('devel', branch='master')
    version('20200401', commit='7ebe2ede05a6ee366d93a7a993db69a99943a68f')

    def setup_build_environment(self, env):

        binpath = os.path.join(self.stage.source_path, 'bin')
        libpath = os.path.join(self.stage.source_path, 'lib')

        env.set('BINDIR', binpath)
        env.set('LIBDIR', libpath)

    def build(self, spec, prefix):

        binpath = os.path.join(self.stage.source_path, 'bin')
        libpath = os.path.join(self.stage.source_path, 'lib')

        mkdir(binpath)
        mkdir(libpath)

        make()

    def install(self, spec, prefix):

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
