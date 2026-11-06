# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DupeToolUser(Package):
    """Links against the newer dupe-tool."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dupe-tool-user-1.0.tar.gz"

    version("1.0", md5="11112222333344445555666677778888")

    depends_on("dupe-tool@2.0", type=("link", "run"))
