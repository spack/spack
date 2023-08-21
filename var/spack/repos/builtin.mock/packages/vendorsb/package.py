# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vendorsb(Package):
    """A package that vendors another, and thus conflicts with it"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/b-1.0.tar.gz"

    version("1.1", md5="0123456789abcdef0123456789abcdef")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    # b is not a dependency
    conflicts("b", when="@=1.1")
