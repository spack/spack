# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedToolClient(Package):
    """Links deprecated-tool-lib, and needs deprecated-tool at build time."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-tool-client-1.0.tar.gz"

    version("1.0", md5="99998888777766665555444433332222")

    depends_on("deprecated-tool-lib")
    depends_on("deprecated-tool", type="build")
