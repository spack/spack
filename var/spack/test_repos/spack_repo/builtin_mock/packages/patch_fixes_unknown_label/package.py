# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class PatchFixesUnknownLabel(Package):
    """Package with a patch that fixes a label no deprecated() directive declares."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-fixes-unknown-label-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    deprecated("@1.0", reason="vuln", severity="high", labels=["CVE-2026-1234"])

    patch("cve.patch", fixes=["CVE-2026-9999"])
