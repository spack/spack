# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class UnifyBuildDepsC(Package):
    tags = ["build-tools"]
    url = "http://example.com/unify-build-deps-c-1.0.tar.gz"
    version("2.0", sha256="d41d8cd98f00b204e9800998ecf8427ed41d8cd98f00b204e9800998ecf8427e")
    version("1.0", sha256="d41d8cd98f00b204e9800998ecf8427ed41d8cd98f00b204e9800998ecf8427e")
