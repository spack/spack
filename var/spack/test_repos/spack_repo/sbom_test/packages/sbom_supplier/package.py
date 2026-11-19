# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SbomSupplier(Package):
    """Declares a supplier, a license, and a checksummed tarball version."""

    homepage = "https://example.com/sbom-supplier"
    url = "https://example.com/sbom-supplier-9.9.tar.gz"
    git = "https://github.com/example/sbom-supplier.git"

    supplier = "Person: Unit Test"

    license("MIT")

    version("1.0", sha256="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
