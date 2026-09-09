# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedDual(Package):
    """Package using both version(..., deprecated=True) and the deprecated() directive."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-dual-1.0.tar.gz"

    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version(
        "1.0",
        sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        deprecated=True,
    )

    # Also annotate @1.0 with the new directive for reason/severity metadata
    deprecated("@1.0", reason="vuln", severity="high")
