# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ImpliedBoolean(AutotoolsPackage):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    variant("v1", default="no",
            description="One choice is an implied boolean value in YAML 1.1",
            values=('no', 'foo1', 'foo2', 'foo3'), multi=False)

    def install(self, spec, prefix):
        pass
