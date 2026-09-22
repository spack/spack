# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedWithLabels(Package):
    """Package using the deprecated() directive with advisory labels."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-with-labels-1.0.tar.gz"

    version("3.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    deprecated("@3.0", reason="vuln", severity="critical", labels=["CVE-2026-0001"])
    deprecated(
        "@2.0", reason="vuln", severity="critical", labels=["CVE-2026-0002", "GHSA-aaaa-bbbb-cccc"]
    )
    deprecated("@1.0", reason="unspecified", severity="critical", msg="use @3.0 instead")
