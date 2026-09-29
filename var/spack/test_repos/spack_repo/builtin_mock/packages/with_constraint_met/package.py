# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class WithConstraintMet(Package):
    """Package that tests True when specs on directives."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.0.tar.gz"

    version("2.0", md5="0123456789abcdef0123456789abcdef")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("c", type="build")

    with when("@1.0"):
        depends_on("pkg-b")
        conflicts("%gcc", when="+foo")

    with when("@0.14: ^pkg-b@:4.0"):
        depends_on("pkg-c", when="@:15 ^pkg-b@3.8:")

    # Direct dependency in a "when" context manager
    with when("%pkg-b"):
        depends_on("pkg-e")

    # More complex dependency with nested contexts
    with when("%pkg-c"):
        with when("@2 %pkg-b@:4.0"):
            depends_on("pkg-e", when="%c=gcc")

    # Nested ^pkg-c followed by %pkg-c
    with when("^pkg-c"):
        with when("%pkg-c"):
            depends_on("pkg-e")

    # Nested ^pkg-c followed by ^pkg-c %gcc
    with when("^pkg-c"):
        with when("^pkg-c %gcc"):
            depends_on("pkg-e")
