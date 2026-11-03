# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class ConditionalVariantPkgDependent(Package):
    """Package with dependency on package with conditional variants."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/archive-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("a", values=("v1", "v2", "v3"), multi=False, default="v1")

    depends_on("conditional-variant-pkg@2.0 ~version_based", when="a=v1")
    depends_on("conditional-variant-pkg@2.0 +version_based +variant_based", when="a=v2")
    depends_on("conditional-variant-pkg@2.0 +version_based +variant_based +two_whens", when="a=v3")
