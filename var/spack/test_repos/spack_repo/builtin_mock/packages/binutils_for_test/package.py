# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class BinutilsForTest(Package):
    """A mock binutils-like package with a pure link dependency on zlib.
    Used to test that transitive link-only deps of compiler run-deps are
    not forced onto packages that use the compiler as a build dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/binutils-for-test-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("c", type="build")
    depends_on("zlib", type="link")
