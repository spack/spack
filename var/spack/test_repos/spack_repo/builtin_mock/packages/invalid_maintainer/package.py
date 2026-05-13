# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class InvalidMaintainer(Package):
    """Package with invalid maintainers (placeholders)."""

    url = "https://www.example.com/archive/v1.0.tar.gz"

    maintainers("github_user1", "github_user2")

    version("1.0", sha256="abcdefg")
