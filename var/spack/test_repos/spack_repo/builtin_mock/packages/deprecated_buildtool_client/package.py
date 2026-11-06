# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedBuildtoolClient(Package):
    """Build-depends on a tool that transitively pulls in a deprecated runtime dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-buildtool-client-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    depends_on("deprecated-buildtool", type="build")
