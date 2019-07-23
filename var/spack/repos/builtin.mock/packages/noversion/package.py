# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Noversion(Package):
    """Simple package with no version."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    def install(self, spec, prefix):
        touch(join_path(prefix, 'an_installation_file'))
