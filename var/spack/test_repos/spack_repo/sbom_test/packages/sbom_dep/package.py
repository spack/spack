# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SbomDep(Package):
    """Dependency of sbom-root."""

    homepage = "https://example.com/sbom-dep"
    url = "https://example.com/sbom-dep-2.0.tar.gz"
    git = "https://github.com/dep-org/sbom-dep.git"

    version("2.0", sha256="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
