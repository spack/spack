# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsigsegv(AutotoolsPackage):
    """GNU libsigsegv is a library for handling page faults in user mode."""

    homepage = "https://www.gnu.org/software/libsigsegv/"
    url      = "https://ftpmirror.gnu.org/libsigsegv/libsigsegv-2.11.tar.gz"

    patch('patch.new_config_guess', when='@2.10')

    variant("shared", default=True, description="Enable shared libraries")
    version('2.11', 'a812d9481f6097f705599b218eea349f')
    version('2.10', '7f96fb1f65b3b8cbc1582fb7be774f0f')

    def flag_handler(self, name, flags):
        if name == 'ldflags' and self.spec.satisfies('~shared platform=cray'):
            # Cray compiler wrappers link -lc. Libsigsegv links -lpthreads.
            # linking -lc -lpthreads statically errors on multiple definitions.
            flags.append('-Wl,--allow-multiple-definition')
        return(flags, None, None)

    def configure_args(self):
        args = []
        if "+shared" in self.spec:
            args.append("--enable-shared")
        else:
            args.append("--disable-shared")
        return args
