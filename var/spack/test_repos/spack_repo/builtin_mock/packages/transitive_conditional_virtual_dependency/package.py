# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.bundle import BundlePackage

from spack.package import *


class TransitiveConditionalVirtualDependency(BundlePackage):
    """Depends on a package with a conditional virtual dependency."""

    homepage = "https://dev.null"

    version("1.0")
    depends_on("conditional-virtual-dependency")
