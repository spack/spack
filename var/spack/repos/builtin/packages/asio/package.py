# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Asio(AutotoolsPackage):
    """C++ library for network and low-level I/O programming."""

    homepage = "https://think-async.com/Asio/"
    url = "https://github.com/chriskohlhoff/asio/archive/asio-1-18-2.tar.gz"
    git = "https://github.com/chriskohlhoff/asio.git"
    maintainers("msimberg")

    version("1.21.0", sha256="5d2d2dcb7bfb39bff941cabbfc8c27ee322a495470bf0f3a7c5238648cf5e6a9")
    version("1.20.0", sha256="34a8f07be6f54e3753874d46ecfa9b7ab7051c4e3f67103c52a33dfddaea48e6")
    version("1.19.2", sha256="5ee191aee825dfb1325cbacf643d599b186de057c88464ea98f1bae5ba4ff47a")
    version("1.19.1", sha256="2555e0a29256de5c77d6a34b14faefd28c76555e094ba0371acb0b91d483520e")
    version("1.19.0", sha256="11bc0e22fcdfb3f0b77574ac33760a3592c0dac7e7eece7668b823c158243629")
    version("1.18.2", sha256="8d67133b89e0f8b212e9f82fdcf1c7b21a978d453811e2cd941c680e72c2ca32")
    version("1.18.1", sha256="39c721b987b7a0d2fe2aee64310bd128cd8cc10f43481604d18cb2d8b342fd40")
    version("1.18.0", sha256="820688d1e0387ff55194ae20036cbae0fb3c7d11b7c3f46492369723c01df96f")
    version("1.17.0", sha256="46406a830f8334b3789e7352ed7309a39c7c30b685b0499d289eda4fd4ae2067")
    version("1.16.1", sha256="e40bbd531530f08318b7c7d7e84e457176d8eae6f5ad2e3714dc27b9131ecd35")
    version("1.16.0", sha256="c87410ea62de6245aa239b9ed2057edf01d7f66acc3f5e50add9a29343c87512")

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

    variant("separate_compilation", default=False, description="Compile Asio sources separately")

    variant("boost_coroutine", default=False, description="Enable support for Boost.Coroutine.")
    depends_on("boost +context +coroutine", when="+boost_coroutine")

    variant("boost_regex", default=False, description="Enable support for Boost.Regex.")
    depends_on("boost +regex", when="+boost_regex")

    for std in stds:
        depends_on("boost cxxstd=" + std, when="cxxstd={0} ^boost".format(std))

    def configure_args(self):
        variants = self.spec.variants

        args = ["CXXFLAGS=-std=c++{0}".format(variants["cxxstd"].value)]

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
