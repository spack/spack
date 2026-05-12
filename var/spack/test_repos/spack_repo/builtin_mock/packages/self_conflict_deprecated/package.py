# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class SelfConflictDeprecated(Package):
    """Package with a deprecated variant and a conflict on the same (post-rewrite) constraint."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/self-conflict-deprecated-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    variant(
        "libs",
        default="shared",
        values=("shared", "static"),
        multi=True,
        description="Build shared or static libraries",
    )

    # +shared is deprecated and conflicts: after rewriting +shared -> libs=shared, the
    # conflict("libs=shared") should fire and make libs=shared an unsatisfiable spec.
    deprecated("+shared", reason="rename", replace={"+shared": "libs=shared"})
    conflicts("libs=shared", msg="libs=shared conflict fired")
