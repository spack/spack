# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from ...build_systems.bundle import BundlePackage


class AttributesFooApp(BundlePackage):
    version("1.0")
    depends_on("bar")
    depends_on("baz")
