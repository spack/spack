# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Baz(Package):
    homepage = "https://www.example.com"
    has_code = False
    version("1.0")
    version("2.0")
    depends_on("foo@1", when="@1")
    depends_on("bar@1", when="@1")
    depends_on("foo@2", when="@2")
    depends_on("bar@2", when="@2")

    def install(self, spec, prefix):
        touch(prefix.baz)
