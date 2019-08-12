# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bats(Package):
    """Bats is a TAP-compliant testing framework for Bash."""

    homepage = "https://github.com/sstephenson/bats"
    url      = "https://github.com/sstephenson/bats/archive/v0.4.0.tar.gz"

    version('0.4.0', 'aeeddc0b36b8321930bf96fce6ec41ee')

    def install(self, spec, prefix):
        bash = which("bash")
        bash('install.sh', prefix)
