# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

from spack.package import *


class Libzmq(AutotoolsPackage):
    """The ZMQ networking/concurrency library and core API"""

    homepage = "https://zguide.zeromq.org/"
    git = "https://github.com/zeromq/libzmq.git"

    def url_for_version(self, ver):
        if ver <= Version("4.1.4"):
            return f"http://download.zeromq.org/zeromq-{ver}.tar.gz"
        return f"https://github.com/zeromq/libzmq/releases/download/v{ver}/zeromq-{ver}.tar.gz"

    maintainers("dennisklein")
    test_requires_compiler = True

    license("MPL-2.0")

    version("master", branch="master")
    version("4.3.5", sha256="6653ef5910f17954861fe72332e68b03ca6e4d9c7160eb3a8de5a5a913bfab43")
    version("4.3.4", sha256="c593001a89f5a85dd2ddf564805deb860e02471171b3f204944857336295c3e5")
    version("4.3.3", sha256="9d9285db37ae942ed0780c016da87060497877af45094ff9e1a1ca736e3875a2")

    # Policy: https://spack.readthedocs.io/en/latest/packaging_guide.html#deprecating-old-versions
    #
    # Version   Deprecation Reason
    # =======   ===============================================================================
    # @:4.3.2   https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-13132,
    #           https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15166,
    #           https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-36400,
    #           https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-20234,
    #           https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-20235,
    #           https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-20236,
    #           https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-20237,
    #           poor modern compiler support, see conflicts
    # @:4.3.1   https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-6250
    #   @:4.2   legacy release 2018 (https://github.com/zeromq/libzmq/releases/tag/v4.2.5)
    #   @:4.1   legacy release 2016 (http://wiki.zeromq.org/intro:get-the-software),
    #           http://download.zeromq.org/zeromq-4.1.4.tar.gz -> 503 Service Unavailable
    #   @:4.0   legacy release 2016 (http://wiki.zeromq.org/intro:get-the-software),
    #           http://download.zeromq.org/zeromq-4.0.7.tar.gz -> 503 Service Unavailable

    with default_args(deprecated=True):
        version("4.3.2", sha256="ebd7b5c830d6428956b67a0454a7f8cbed1de74b3b01e5c33c5378e22740f763")
        version("4.3.1", sha256="bcbabe1e2c7d0eec4ed612e10b94b112dd5f06fcefa994a0c79a45d835cd21eb")
        version("4.3.0", sha256="8e9c3af6dc5a8540b356697081303be392ade3f014615028b3c896d0148397fd")
        version("4.2.5", sha256="cc9090ba35713d59bb2f7d7965f877036c49c5558ea0c290b0dcc6f2a17e489f")
        version("4.2.2", sha256="5b23f4ca9ef545d5bd3af55d305765e3ee06b986263b31967435d285a3e6df6b")
        version("4.1.4", sha256="e99f44fde25c2e4cb84ce440f87ca7d3fe3271c2b8cfbc67d55e4de25e6fe378")
        version("4.1.2", sha256="f9162ead6d68521e5154d871bac304f88857308bb02366b81bb588497a345927")
        version("4.1.1", sha256="43d61e5706b43946aad4a661400627bcde9c63cc25816d4749c67b64c3dab8db")
        version("4.0.7", sha256="e00b2967e074990d0538361cc79084a0a92892df2c6e7585da34e4c61ee47b03")
        version("4.0.6", sha256="28a2a9c9b77014c39087a498942449df18bb9885cdb63334833525a1d19f2894")
        version("4.0.5", sha256="3bc93c5f67370341428364ce007d448f4bb58a0eaabd0a60697d8086bc43342b")

    variant("docs", default=False, description="Build documentation")
    variant("drafts", default=False, description="Build and install draft classes and methods")
    variant(
        "libbsd",
        when="@4.3.3:",
        default=(sys.platform != "darwin"),
        description="Use strlcpy from libbsd (will use own implementation if false)",
    )
    variant(
        "libsodium",
        default=True,
        description="Build with message encryption support via libsodium",
    )
    variant("libunwind", default=False, description="Build with libunwind support")

    conflicts("%gcc@8:", when="@:4.2.2")
    conflicts("%gcc@11:", when="@:4.3.2")

    with default_args(type="build"):
        depends_on("pkgconfig")
        with when("@master"):
            depends_on("autoconf")
            depends_on("automake")
            depends_on("libtool")
            depends_on("ruby-asciidoctor")

    depends_on("libbsd", when="+libbsd")
    depends_on("libsodium", when="+libsodium")
    depends_on("libsodium@:1.0.3", when="@:4.1.2 +libsodium")
    depends_on("libunwind", when="+libunwind")

    # Fix aggressive compiler warning false positive
    patch(
        "https://github.com/zeromq/libzmq/commit/92b2c38a2c51a1942a380c7ee08147f7b1ca6845.patch?full_index=1",
        sha256="310b8aa57a8ea77b7ac74debb3bf928cbafdef5e7ca35beaac5d9c61c7edd239",
        when="@4.3.3:4.3.4",
    )
    # Fix build issues with gcc-12
    patch(
        "https://github.com/zeromq/libzmq/pull/4334.patch?full_index=1",
        sha256="edca864cba914481a5c97d2e975ba64ca1d2fbfc0044e9a78c48f1f7b2bedb6f",
        when="@4.3.4",
    )
    # Fix static assertion failure with gcc-13
    patch(
        "https://github.com/zeromq/libzmq/commit/438d5d88392baffa6c2c5e0737d9de19d6686f0d.patch?full_index=1",
        sha256="e15a8bfe8131f3e648fd79f3c1c931f99cd896b2733a7df1760f5b4354a0687c",
        when="@4.3.3:4.3.4",
    )

    INCLUDEDIR = "include"
    LIBDIR = "lib"
    DATAROOTDIR = "share"
    MANDIR = "man"
    PKGCONFIGDIR = "pkgconfig"

    @when("@master")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def configure_args(self):
        args = [
            f"--includedir={join_path(self.prefix, self.INCLUDEDIR)}",
            f"--libdir={join_path(self.prefix, self.LIBDIR)}",
            f"--datarootdir={join_path(self.prefix, self.DATAROOTDIR)}",
            f"--mandir={join_path(self.prefix, self.DATAROOTDIR, self.MANDIR)}",
            f"--with-pkgconfigdir={join_path(self.prefix, self.LIBDIR, self.PKGCONFIGDIR)}",
        ]
        args += self.with_or_without("docs")
        args += self.enable_or_disable("drafts")
        args += self.enable_or_disable("libbsd")
        args += self.with_or_without("libsodium")
        args += self.enable_or_disable("libunwind")
        # the package won't compile with newer compilers because warnings
        # are converted to errors. Hence, disable such conversion.
        if self.spec.version >= Version("4.2.3"):
            args.append("--disable-Werror")
        if self.spec.compiler.name == "clang":
            args.append("CFLAGS=-Wno-gnu")
            args.append("CXXFLAGS=-Wno-gnu")
        return args

    @run_after("configure")
    @on_package_attributes(run_tests=True)
    def check_configure(self):
        """sanity checks to avoid mistakes like in https://github.com/spack/spack/issues/40455"""
        config_log = open("config.log", "r").read()
        macros = []
        if self.spec.satisfies("+drafts"):
            macros.append("#define ZMQ_BUILD_DRAFT_API 1")
        if self.spec.satisfies("+libbsd"):
            macros.append("#define ZMQ_HAVE_LIBBSD 1")
        if self.spec.satisfies("+libsodium"):
            macros.append("#define ZMQ_USE_LIBSODIUM 1")
        if self.spec.satisfies("+libunwind"):
            macros.append("#define HAVE_LIBUNWIND 1")
        # https://github.com/zeromq/libzmq/commit/ff47aeb791e134a78bc386e12eea67618e0bf2f7
        # Since 4.3.5 the curve feature is only available via libsodium backend
        if not self.spec.satisfies("@4.3.5:~libsodium"):
            macros.append("#define ZMQ_HAVE_CURVE 1")
        for macro in macros:
            if not re.search(macro, config_log):
                raise RuntimeError(f"Expected '{macro}' in config.log")

    sanity_check_is_file = [
        join_path(INCLUDEDIR, "zmq.h"),
        join_path(LIBDIR, "libzmq.so"),
        join_path(LIBDIR, PKGCONFIGDIR, "libzmq.pc"),
    ]

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_presence_of_files(self):
        """check presence of important (conditional) files"""
        if self.spec.satisfies("+docs"):
            assert os.path.exists(
                join_path(self.prefix, self.DATAROOTDIR, self.MANDIR, "man7", "zmq.7")
            )

    def _compiled_executable(self, source_code):
        """compile the given C source code as executable"""
        exe = f"test_{abs(hash(source_code)):08x}"
        source_file = f"{exe}.c"
        open(source_file, "w").write(source_code)
        Executable(self.compiler.cc)(
            f"-L{join_path(self.prefix, self.LIBDIR)}",
            "-lzmq",
            f"-I{join_path(self.prefix, self.INCLUDEDIR)}",
            source_file,
            "-o",
            exe,
        )
        return which(exe)

    def test_basic_usage(self):
        """check basic functionality by printing the ZMQ version using the library"""
        out = self._compiled_executable(
            r"""
#include <stdio.h>
#include <stdlib.h>
#include <zmq.h>

int main() {
    int major, minor, patch;
    zmq_version(&major, &minor, &patch);
    printf("%d.%d.%d", major, minor, patch);
    return EXIT_SUCCESS;
}
            """.strip()
        )(output=str.split, error=str.split)
        if not self.spec.satisfies("@master"):
            check_outputs(str(self.version), out)
