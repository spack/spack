# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedOldStyle(Package):
    """Package using only version(..., deprecated=True), without the deprecated() directive."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-old-style-1.0.tar.gz"

    version(
        "1.0",
        sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        deprecated=True,
    )
    version("0.9", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
