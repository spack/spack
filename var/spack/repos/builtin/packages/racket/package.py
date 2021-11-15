# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Racket(Package):
    """The Racket programming language."""

    homepage = "https://www.racket-lang.org"
    url      = "https://download.racket-lang.org/releases/8.3/installers/racket-src.tgz"

    maintainers = ['arjunguha']

    version('8.3.0', 'c4af1a10b957e5fa0daac2b5ad785cda79805f76d11482f550626fa68f07b949')

    depends_on('libffi', type=('build', 'link', 'run'))
    depends_on('patchutils')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        with working_dir('src'):
            configure = Executable('./configure')
            configure("--prefix", prefix)

    def build(self, spec, prefix):
        with working_dir('src'):
            make()

    def install(self, spec, prefix):
        with working_dir('src'):
            make('install')
