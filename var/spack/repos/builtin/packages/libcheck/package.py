# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcheck(CMakePackage):
    """A unit testing framework for C."""

    homepage = "https://libcheck.github.io/check/index.html"
    url      = "https://github.com/libcheck/check/releases/download/0.12.0/check-0.12.0.tar.gz"

    version('0.12.0', '31b17c6075820a434119592941186f70')
    version('0.11.0', '9b90522b31f5628c2e0f55dda348e558')
    version('0.10.0', '53c5e5c77d090e103a17f3ed7fd7d8b8')
