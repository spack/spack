# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bar(Package):
    homepage = "https://www.example.com"
    has_code = False
    variant("compat", default=True)
    version("1.0.0")
    version("1.0.1")
    can_splice("bar@1.0.0 +compat", when="@1.0.1 +compat")
    version("1.0.2")
    can_splice("bar@1.0.0:1.0.1", when="@1.0.2 +compat")
    version("2.0.0")
    depends_on("foo@1", when="@1")
    depends_on("foo@2", when="@2")

    def install(self, spec, prefix):
        touch(prefix.bar)
