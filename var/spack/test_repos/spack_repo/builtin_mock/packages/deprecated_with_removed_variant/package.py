# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedWithRemovedVariant(Package):
    """Package where ~shared is deprecated with no replacement (always builds shared now)."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-with-removed-variant-1.0.tar.gz"

    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    variant(
        "shared", default=True, values=(True, False), description="Build shared or static libs"
    )

    deprecated(
        "~shared",
        reason="maintenance",
        replace={"~shared": None},
        msg="Static builds are no longer supported.",
    )
