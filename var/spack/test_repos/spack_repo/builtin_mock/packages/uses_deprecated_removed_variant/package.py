# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class UsesDeprecatedRemovedVariant(Package):
    """Package that depends on deprecated-with-removed-variant with the removed ~shared."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/uses-deprecated-removed-variant-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    depends_on("deprecated-with-removed-variant~shared")
