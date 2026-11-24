# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SbomRoot(Package):
    """Depends on sbom-dep, with a different supplier and checksum."""

    homepage = "https://example.com/sbom-root"
    url = "https://example.com/sbom-root-1.0.tar.gz"
    git = "https://github.com/root-org/sbom-root.git"

    version("1.0", sha256="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    depends_on("sbom-dep")
