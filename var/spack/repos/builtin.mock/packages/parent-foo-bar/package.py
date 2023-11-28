# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ParentFooBar(Package):
    """This package has a variant "bar", which is True by default, and depends on another
    package which has the same variant defaulting to False.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/parent-foo-bar-1.0.tar.gz"

    version("1.0", md5="abcdefg0123456789abcdefghfedcba0")

    variant("foo", default=True, description="")
    variant("bar", default=True, description="")

    depends_on("dependency-foo-bar")
