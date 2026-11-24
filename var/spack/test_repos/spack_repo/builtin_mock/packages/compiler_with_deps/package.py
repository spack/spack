# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.compiler import CompilerPackage
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class CompilerWithDeps(CompilerPackage, Package):
    """A mock compiler that has a run+link dependency on binutils-for-test,
    which itself has a pure link dependency on zlib. Used to test that
    transitive link-only deps of compiler run-deps are not forced onto
    packages that use this compiler as a build dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/compiler-with-deps-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    provides("c")

    depends_on("c", type="build")
    depends_on("binutils-for-test", type=("run", "link"))

    c_names = ["compiler-with-deps-cc"]
    compiler_version_regex = r"([0-9.]+)"
    compiler_version_argument = "--version"

    compiler_wrapper_link_paths = {"c": "compiler-with-deps/cc"}
