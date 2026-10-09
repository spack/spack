# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedPatched(Package):
    """Package with deprecated versions and a patch that fixes some of their labels."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-patched-1.0.tar.gz"

    version("1.1", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("0.9", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    deprecated("@1.0", reason="vuln", severity="high", labels=["CVE-2026-1234"])
    deprecated("@0.9", reason="vuln", severity="high", labels=["CVE-2026-1234", "CVE-2026-5678"])

    patch("cve-2026-1234.patch", when="@:1.0", fixes=["CVE-2026-1234"])
