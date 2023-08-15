# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gcc(Package):
    """Simple compiler package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/gcc-1.0.tar.gz"

    version("12.2.0", md5="0123456789abcdef0123456789abcdef")
    version("12.1.0", md5="abcdef0123456789abcdef0123456789", preferred=True)
    version("3.0", md5="def0123456789abcdef0123456789abc")
    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("conflict", when="@3.0")

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(prefix.bin)
        with open(prefix.bin.gcc, "w") as f:
            f.write('#!/bin/bash\necho "%s"' % str(spec.version))
        set_executable(prefix.bin.gcc)
