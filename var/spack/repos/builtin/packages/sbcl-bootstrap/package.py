# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *
from spack.util.environment import set_env


class SbclBootstrap(Package):
    """Steel Bank Common Lisp (SBCL) is a high performance Common Lisp compiler.
    It is open source / free software, with a permissive license. In addition
    to the compiler and runtime system for ANSI Common Lisp, it provides an
    interactive environment including a debugger, a statistical profiler, a
    code coverage tool, and many other extensions.
    """

    homepage = "https://www.sbcl.org/"

    maintainers("ashermancinelli")

    # NOTE: The sbcl homepage lists
    # while the sourceforge repo lists "Public Domain, MIT License", the
    # COPYING file distributed with the source code contains this message:
    #
    # Thus, there are no known obstacles to copying, using, and modifying
    # SBCL freely, as long as copyright notices of MIT, Symbolics, Xerox and
    # Gerd Moellmann are retained.
    #
    # MIT seems the most appropriate, but if we can add more context to this
    # license message, then we should.
    license("MIT", checked_by="ashermancinelli")

    # By checking objdump -T of the sbcl binary in each prebuilt tarball, I
    # found the latest reference to glibc for each version.
    sbcl_releases = {
        "2.3.11": {
            "x86_64": "98784b04f68882b887984242eef73dbb092ec5c778dd536b2c60846715e03f3c",
            "min_glibc": "2.34",
        },
        "2.0.11": {
            "x86_64": "b7e61bc6b8d238f8878e660bc0635e99c2ea1255bfd6153d702fe9a00f8138fd",
            "min_glibc": "2.28",
        },
        "1.4.16": {
            "x86_64": "df3d905d37656a7eeeba72d703577afc94a21d756a4dde0949310200f82ce575",
            "min_glibc": "2.14",
        },
        "1.4.2": {
            "aarch64": "ddac6499f36c18ecbce9822a53ef3914c0def5276a457446a456c62999b16d36",
            "min_glibc": "2.17",
        },
        "1.3.21": {
            "x86_64": "c1c3e17e1857fb1c22af575941be5cd1d5444b462397b1b3c9f3877aee2e814b",
            "min_glibc": "2.3",
        },
    }

    os = platform.system().lower()
    target = platform.machine().lower()

    for ver in sbcl_releases:
        if target in sbcl_releases[ver]:
            version(ver, sha256=sbcl_releases[ver][target])
            if "min_glibc" in sbcl_releases[ver]:
                conflicts(
                    "glibc@:{0}".format(sbcl_releases[ver]["min_glibc"]), when="@{0}".format(ver)
                )

    supported_sysinfo_msg = "linux x86_64 is the only supported platform"
    for sysinfo in ["platform=darwin", "platform=windows", "target=ppc64le"]:
        conflicts(sysinfo, msg=supported_sysinfo_msg)

    def url_for_version(self, version):
        if self.os != "linux":
            return None
        target = platform.machine().lower()
        sbcl_targets = {"aarch64": "arm64", "x86_64": "x86-64"}
        if target not in sbcl_targets:
            return None
        sbcl_url = "https://sourceforge.net/projects/sbcl/files/sbcl/{version}/sbcl-{version}-{target}-linux-binary.tar.bz2"
        return sbcl_url.format(version=version, target=sbcl_targets[target])

    def install(self, spec, prefix):
        sh = which("sh")
        with set_env(INSTALL_ROOT=self.spec.prefix):
            sh("install.sh")
