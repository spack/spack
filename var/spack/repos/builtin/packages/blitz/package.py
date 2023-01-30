# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blitz(AutotoolsPackage):
    """N-dimensional arrays for C++"""

    homepage = "https://github.com/blitzpp/blitz"
    url = "https://github.com/blitzpp/blitz/archive/1.0.2.tar.gz"

    version("1.0.2", sha256="500db9c3b2617e1f03d0e548977aec10d36811ba1c43bb5ef250c0e3853ae1c2")

    depends_on("python@3:", type="build")

    build_targets = ["lib"]

    def check(self):
        make("check-testsuite")
        make("check-examples")
