# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class JustTestingTravisCli(Package):
    """Not a real package just a test"""
    homepage = "https://www.github.com"
    url      = "https://github.com/Mentors4EDU/just-testing-travis-cli/releases/download/v1.0/just-testing-travis-cli.tar.bz2"

    maintainers = ['Mentors4EDU']

    version('1.0', sha256='4b9c166569c735772fe1b3177f3f45fb7a06de65e27a2bba91d0688c96a3fe3d')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
