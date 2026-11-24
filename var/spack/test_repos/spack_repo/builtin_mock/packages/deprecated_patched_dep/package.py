# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedPatchedDep(Package):
    """Package with a deprecated version, fixed only by a patch that a dependent applies."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-patched-dep-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    deprecated("@1.0", reason="vuln", severity="high", labels=["CVE-2026-4321"])
