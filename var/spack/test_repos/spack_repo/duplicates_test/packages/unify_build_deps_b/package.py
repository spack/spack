# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class UnifyBuildDepsB(Package):
    url = "http://example.com/unify-build-deps-b-1.0.tar.gz"
    version("1.0", sha256="d41d8cd98f00b204e9800998ecf8427ed41d8cd98f00b204e9800998ecf8427e")

    depends_on("unify-build-deps-c@2", type="run")
