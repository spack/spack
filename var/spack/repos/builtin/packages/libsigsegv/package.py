# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsigsegv(AutotoolsPackage):
    """GNU libsigsegv is a library for handling page faults in user mode."""

    homepage = "https://www.gnu.org/software/libsigsegv/"
    url      = "https://ftpmirror.gnu.org/libsigsegv/libsigsegv-2.11.tar.gz"

    patch('patch.new_config_guess', when='@2.10')

    version('2.11', 'a812d9481f6097f705599b218eea349f')
    version('2.10', '7f96fb1f65b3b8cbc1582fb7be774f0f')

    def configure_args(self):
        return ['--enable-shared']
