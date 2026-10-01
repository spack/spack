# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class RpathLeaf(Package):
    """Package with a lib directory, used as a link dependency in splicing tests"""

    homepage = "http://www.example.com"
    has_code = False

    version("1.0")

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        touch(prefix.lib.join("libleaf.so"))
