# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack import *


class Asio(AutotoolsPackage):
    """C++ library for network and low-level I/O programming."""

    homepage = "https://think-async.com/Asio/"
    url = "https://github.com/chriskohlhoff/asio/archive/1.18.2.tar.gz"
    git = "https://github.com/chriskohlhoff/asio.git"
    maintainers = ["msimberg"]

    version(
        "1.18.2",
        sha256="8d67133b89e0f8b212e9f82fdcf1c7b21a978d453811e2cd941c680e72c2ca32",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")

    stds = ("11", "14", "17", "2a")
    variant(
        "cxxstd",
        default="11",
        values=stds,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant(
        "separate_compilation",
        default=False,
        description="Compile Asio sources separately",
    )

    variant(
        "boost_coroutine",
        default=False,
        description="Enable support for Boost.Coroutine.",
    )
    depends_on("boost +context +coroutine", when="+boost_coroutine")

    variant("boost_regex", default=False, description="Enable support for Boost.Regex.")
    depends_on("boost +regex", when="+boost_regex")

    for std in stds:
        depends_on("boost cxxstd=" + std, when="cxxstd={0} ^boost".format(std))

    def configure_args(self):
        variants = self.spec.variants

        args = [
            "CXXFLAGS=-std=c++{0}".format(variants["cxxstd"].value),
        ]

        if variants["separate_compilation"].value:
            args.append("--enable-separate-compilation")

        if variants["boost_coroutine"].value:
            args.append("--enable-boost-coroutine")

        if variants["boost_coroutine"].value or variants["boost_regex"].value:
            args.append("--with-boost={self.spec['boost'].prefix}")

        return args

    def url_for_version(self, version):
        return "https://github.com/chriskohlhoff/asio/archive/asio-{0}.tar.gz".format(
            version.dashed
        )

    @property
    def configure_directory(self):
        return os.path.join(self.stage.source_path, "asio")
