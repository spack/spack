# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from urllib.request import pathname2url

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


def make_pkg_tarball(version_str):
    import hashlib

    archive_name = f"smoke1-{version_str}.tgz"
    package_root = os.path.dirname(__file__)
    archive = os.path.join(package_root, archive_name)
    if not os.path.exists(archive):
        import tarfile

        with tarfile.open(archive, "w|gz") as tgz:
            tgz.add(os.path.join(package_root, "smoke1-src"), arcname=".")
    sha256_hash = hashlib.sha256()

    with open(archive, "rb") as f:
        chunked_data = f.read(4096)
        while chunked_data:
            sha256_hash.update(chunked_data)
            chunked_data = f.read(4096)
    return sha256_hash.hexdigest()


class Smoke1(CMakePackage):
    """Smoke test - compile and run a simple CMake project
    Basic Smoke test - compiles a one file CMake based project into an executable
    that accepts and adds two integer values, reporting the resultant value to stdout
    Behavior validated by a successful run of CMake, compilation, and Spack driven test
    """

    archive_name = "smoke1-0.1.tgz"

    homepage = "https://spack.io"
    url = "file:" + pathname2url(os.path.join(os.path.dirname(__file__), archive_name))

    maintainers("spack")

    license("MIT")

    version("0.1", sha256=make_pkg_tarball("0.1"))

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    def test_basic(self):
        exe_name = join_path(self.prefix.bin, "smoke1")
        exe = which(exe_name, required=True)
        assert "3" in exe("1", "2", output=str)
