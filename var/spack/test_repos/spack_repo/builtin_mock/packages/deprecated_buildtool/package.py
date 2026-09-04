# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedBuildtool(Package):
    """A build tool with a deprecated runtime dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-buildtool-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    depends_on("deprecated-versions@1.1.0", type="run")
