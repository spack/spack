# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedToolLib(Package):
    """Depends on deprecated-tool at build time; not itself deprecated."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-tool-lib-1.0.tar.gz"

    version("1.0", md5="11112222333344445555666677778888")

    depends_on("deprecated-tool", type="build")
