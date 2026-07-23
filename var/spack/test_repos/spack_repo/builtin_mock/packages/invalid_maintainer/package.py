# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class InvalidMaintainer(Package):
    """Package with invalid maintainers (placeholders)."""

    url = "https://www.invalid-maintainer.org/archive/v1.0.tar.gz"

    maintainers("github_user1", "github_user2")

    version("1.0", sha256="0f22de2391d80d8b393c4f9d11488600126c60ae36ceef780c6a4b3d9dab2e96")
