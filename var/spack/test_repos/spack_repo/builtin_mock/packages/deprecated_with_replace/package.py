# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DeprecatedWithReplace(Package):
    """Package using deprecated() with replace= for pre-solver variant rewriting."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-with-replace-1.0.tar.gz"

    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    variant(
        "libs",
        default="shared",
        values=("shared", "static"),
        multi=True,
        description="Build shared or static libraries",
    )

    # +shared and ~shared are deprecated in favour of libs= multi-valued variant
    deprecated("+shared", reason="rename", replace={"+shared": "libs=shared"})
    deprecated("~shared", reason="rename", replace={"~shared": "libs=static"})
