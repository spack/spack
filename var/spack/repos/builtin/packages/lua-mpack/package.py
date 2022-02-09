# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LuaMpack(LuaPackage):
    """lua bindings to libmpack"""

    homepage = "https://github.com/libmpack/libmpack-lua/"
    url = "https://github.com/libmpack/libmpack-lua/releases/download/1.0.8/libmpack-lua-1.0.8.tar.gz"

    depends_on("msgpack-c")

    rocks_build_flags = ["CFLAGS='-Wno-error=implicit-function-declaration'"]

    version(
        "1.0.9",
        sha256="0fd07e709c3f6f201c2ffc9f77cef1b303b02c12413f0c15670a32bf6c959e9e",
    )
    version(
        "1.0.8",
        sha256="ed6b1b4bbdb56f26241397c1e168a6b1672f284989303b150f7ea8d39d1bc9e9",
    )
    version(
        "1.0.7",
        sha256="68565484a3441d316bd51bed1cacd542b7f84b1ecfd37a8bd18dd0f1a20887e8",
    )
    version(
        "1.0.6-0",
        sha256="9068d9d3f407c72a7ea18bc270b0fa90aad60a2f3099fa23d5902dd71ea4cd5f",
    )
