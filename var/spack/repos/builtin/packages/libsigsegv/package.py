# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsigsegv(AutotoolsPackage):
    """GNU libsigsegv is a library for handling page faults in user mode."""

    homepage = "https://www.gnu.org/software/libsigsegv/"
    url      = "https://ftpmirror.gnu.org/libsigsegv/libsigsegv-2.12.tar.gz"

    version('2.12', sha256='3ae1af359eebaa4ffc5896a1aee3568c052c99879316a1ab57f8fe1789c390b6')
    version('2.11', 'a812d9481f6097f705599b218eea349f')
    version('2.10', '7f96fb1f65b3b8cbc1582fb7be774f0f')

    patch('patch.new_config_guess', when='@2.10')

    def configure_args(self):
        return ['--enable-shared']
