# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class ForcedVariant(Package):
    """Package whose conflict can force a non-default variant value, which in turn
    activates a conditional dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/forced-variant-1.0.tar.gz"

    version("2.0", md5="0123456789abcdef0123456789abcdef")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("foo", default=False)

    conflicts("~foo", when="@2.0")

    depends_on("pkg-b", when="+foo")
