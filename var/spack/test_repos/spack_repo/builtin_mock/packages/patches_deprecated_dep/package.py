# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class PatchesDeprecatedDep(Package):
    """Package that applies a patch fixing a deprecation label of its dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patches-deprecated-dep-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    depends_on(
        "deprecated-patched-dep",
        patches=[patch("cve-2026-4321.patch", when="@1.0", fixes=["CVE-2026-4321"])],
    )
