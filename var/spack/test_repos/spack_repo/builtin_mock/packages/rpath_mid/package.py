# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class RpathMid(Package):
    """Package whose link dependency on rpath-leaf is optional"""

    homepage = "http://www.example.com"
    has_code = False

    version("1.0")

    variant("leaf", default=True, description="Depend on rpath-leaf")

    depends_on("rpath-leaf", when="+leaf")

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        touch(prefix.lib.join("libmid.so"))
