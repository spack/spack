# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DeprecatedVariantPkg(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-variant-pkg-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    # Case 1: deprecated=True (just remove)
    variant("old_flag", default=True, deprecated=True)

    # Case 2: bool variant with mapping
    variant(
        "shared", default=True, deprecated={"+shared": "libs=shared", "~shared": "libs=static"}
    )

    # The replacement variant for shared
    variant("libs", default="shared", values=("shared", "static"), multi=False)

    # Case 3: multi-valued variant with per-value mapping
    variant(
        "old_backends",
        default="none",
        values=("a", "b", "c", "none"),
        multi=True,
        deprecated={
            "old_backends=a": "backends=alpha",
            "old_backends=b": "backends=beta",
            "old_backends=c": "backends=gamma",
        },
    )
    variant("backends", default="none", values=("alpha", "beta", "gamma", "none"), multi=True)
