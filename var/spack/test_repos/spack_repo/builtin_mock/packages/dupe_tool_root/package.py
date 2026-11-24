# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DupeToolRoot(Package):
    """Builds against an older dupe-tool than the one its runtime dependency links against."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dupe-tool-root-1.0.tar.gz"

    version("1.0", md5="abcdefabcdefabcdefabcdefabcdefab")

    depends_on("dupe-tool@1.0", type="build")
    depends_on("dupe-tool-user", type=("link", "run"))
