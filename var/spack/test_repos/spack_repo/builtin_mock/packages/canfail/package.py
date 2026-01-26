# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Canfail(Package):
    """Package which fails install unless a special attribute is set"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"
    succeed = True

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        if not self.succeed:
            raise InstallError("'succeed' was false")
        touch(join_path(prefix, "an_installation_file"))
