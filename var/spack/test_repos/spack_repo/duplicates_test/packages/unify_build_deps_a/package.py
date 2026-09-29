# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class UnifyBuildDepsA(Package):
    """Used to test that we cannot have a build environment with two conflicting versions of
    a package (unify-build-deps-c), even if that package is tagged as a build-tool with duplicates
    allowed."""

    url = "http://example.com/unify-build-deps-a-1.0.tar.gz"
    version("2.0", sha256="d41d8cd98f00b204e9800998ecf8427ed41d8cd98f00b204e9800998ecf8427e")
    version("1.0", sha256="d41d8cd98f00b204e9800998ecf8427ed41d8cd98f00b204e9800998ecf8427e")

    depends_on("unify-build-deps-c@1", type="build")

    # If unify-build-deps-b is used as a build dependency, we cannot unify the build environment.
    depends_on("unify-build-deps-b", type=("build", "run"), when="@1")

    # If unify-build-deps-b is not used as build dependency, we can unify the build environment
    depends_on("unify-build-deps-b", type=("link", "run"), when="@2")
