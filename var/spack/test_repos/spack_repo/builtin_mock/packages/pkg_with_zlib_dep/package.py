# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class PkgWithZlibDep(Package):
    """A minimal mock package that depends on C (build) and zlib (link).
    Used to test that the compiler's transitive link-only deps (reachable
    through its run-dep binutils-for-test -> zlib) are not forced onto
    this package's own zlib dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/pkg-with-zlib-dep-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("c", type="build")
    depends_on("zlib", type="link")
