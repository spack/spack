# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libzip(AutotoolsPackage):
    """libzip is a C library for reading, creating,
    and modifying zip archives."""

    homepage = "https://nih.at/libzip/index.html"
    url = "https://nih.at/libzip/libzip-1.2.0.tar.gz"

    license("BSD-3-Clause")

    version("1.3.2", sha256="ab4c34eb6c3a08b678cd0f2450a6c57a13e9618b1ba34ee45d00eb5327316457")
    version("1.2.0", sha256="6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f")

    depends_on("zlib-api")

    @property
    def headers(self):
        # Up to version 1.3.0 zipconf.h was installed outside of self.prefix.include
        return find_all_headers(
            self.prefix if self.spec.satisfies("@:1.3.0") else self.prefix.include
        )
