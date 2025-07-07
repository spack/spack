# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems import autotools

from spack.package import *


class ArbitraryExtraAttrs(autotools.AutotoolsPackage):
    """Simple package with one optional dependency"""

    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", sha256=64 * "a")

    depends_on("c", type="build")

    parallel = False

    def check(self):
        exampledict = self.spec.extra_attributes["exampledict"]
        assert exampledict == {"a": 1, "b": "2"}

class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def autoreconf(self, pkg, spec, prefix):
        pass

    def configure(self, pkg, spec, prefix):
        pass

    def build(self, pkg, spec, prefix):
        exampledict = spec.extra_attributes["exampledict"]
        assert exampledict == {"a": 1, "b": "2"}

    def install(self, pkg, spec, prefix):
        mkdirp(prefix.bin)
