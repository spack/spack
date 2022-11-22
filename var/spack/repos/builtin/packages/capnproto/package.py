# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Capnproto(AutotoolsPackage):
    """Cap'n'Proto is an insanely fast data interchange
    format and capability-based RPC system
    """

    homepage = "https://capnproto.org"
    url = "https://github.com/capnproto/capnproto/archive/refs/tags/v0.8.0.zip"
    git = "https://github.com/capnproto/capnproto"

    maintainers = ["a.knieps"]

    version("master", branch="master")
    version("0.10.2", sha256="b44e97b391139f35f1749d65d741cc672a72e9396ffb83057bc58f0154ecd18c")
    version("0.10.1", sha256="f68bd25c2e9b2eadee96dced3c2623d4fdba84f1a1135fb0660a3a3bf3cf04bb")
    version("0.10.0", sha256="9fddbe3b13b70e39fda376f8d0bba3e70ddaecaf2fa3962ecb427195d83594cb")
    version("0.9.1", sha256="5d8cc078d866722acf09bd610f3d58565c29986e0a1ca5a4b4cf4a2778b86e41")
    version("0.9.0", sha256="18cf46aa4e05446a3d34bad8d56f9d0c73e72020a2b7548b6ec7cb7b1a828d5b")
    version("0.8.0", sha256="9a5e090b1f3ad39bb47fed5fd03672169493674ce273418b76c868393fced2e4")
    version("0.7.0", sha256="1054a879e174b8f797f1b506fedb14ecba5556c656e33ac51bd0a62bd90f925f")
    version("0.6.1", sha256="db365d1a05afdf82d1069cab9a7fae0e1eafdba26616e8d8bdac3abade71612b")
    version("0.6.0", sha256="5b8401fb30811dcb472791e239a1d034ba890b1d1983cd986a26ccef86f2eb0d")
    version("0.5.3.1", sha256="c3390a67428d78aa4903c8cc519a94d62dd99c84467be539a380e70ac36ee2c4")
    version("0.5.3", sha256="e5c9e7404eba86062f88703ae146c4fa919955ce79b4a1880159dd71476886b7")
    version("0.5.2", sha256="bf3e341bc2c4652da6db08a79f29f658c803e6a8ac10515a702217d2693aae88")
    version("0.5.1.2", sha256="2f24bc302c72762ccaedf47b7d2f835a42184fe0c8eba6537ac1f57f21abbaa3")
    version("0.5.1.1", sha256="b56f8d4e6ccfe480dce20aaf9ccab7e7b5fdc3feeeb0d8016ef00fbc2de82263")
    version("0.4.1.2", sha256="a22b54252f86b5d4edb3770b8d78bf5611dcce34abdc5713af6ff8a093cf9ba6")

    depends_on("zlib", when="+zlib")
    depends_on("openssl", when="+tls")

    depends_on("autoconf", type="build", when="build_system=autotools")
    depends_on("automake", type="build", when="build_system=autotools")
    depends_on("libtool", type="build", when="build_system=autotools")

    variant("zlib", default=True, description="Enable compression")
    variant("tls", default=False, description="Enable TLS support")

    configure_directory = "c++"

    def configure_args(self):
        args = []

        if "+tls" in self.spec:
            args.append("--with-openssl")
        else:
            args.append("--without-openssl")

        if "+zlib" in self.spec:
            args.append("--with-zlib")
        else:
            args.append("--without-zlib")

        return args

    def patch(self):
        # The master branch has version versions of type '0.11-dev', which is incompatible with
        # CMake's find_package call.
        # Therefore, these are patched to the respective release-type versions.
        if self.version == Version("master"):
            filter_file(
                "set\\(VERSION 0\\.(\\d*)\\-dev\\)", "set(VERSION 0.\\1)", "c++/CMakeLists.txt"
            )
            filter_file(
                "AC_INIT\\(\\[Capn Proto\\],\\[0\\.(\\d*)\\-dev\\],\\[capnproto@googlegroups\\.com\\],\\[capnproto\\-c\\+\\+\\]\\)",
                "AC_INIT([Capn Proto],[0.\\1],[capnproto@googlegroups.com],[capnproto-c++])",
                "c++/configure.ac",
            )
