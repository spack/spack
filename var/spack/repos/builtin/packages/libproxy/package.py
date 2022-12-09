# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libproxy(CMakePackage):
    """libproxy is a library that provides automatic proxy configuration
    management."""

    homepage = "https://libproxy.github.io/libproxy/"
    url = "https://github.com/libproxy/libproxy/archive/0.4.15.tar.gz"

    version("0.4.17", sha256="88c624711412665515e2800a7e564aabb5b3ee781b9820eca9168035b0de60a9")
    version("0.4.16", sha256="9e7959d6ae1d6c817f0ac1e253105ce8d99f55d7821c1b6eaef32bf6879c6f0a")
    version("0.4.15", sha256="18f58b0a0043b6881774187427ead158d310127fc46a1c668ad6d207fb28b4e0")
    version("0.4.14", sha256="6220a6cab837a8996116a0568324cadfd09a07ec16b930d2a330e16d5c2e1eb6")
    version("0.4.13", sha256="d610bc0ef81a18ba418d759c5f4f87bf7102229a9153fb397d7d490987330ffd")

    variant("perl", default=False, description="Enable Perl bindings")
    variant("python", default=True, description="Enable Python bindings", when="@0.4.16:")

    depends_on("zlib")
    depends_on("perl", type=("build", "run"), when="+perl")
    depends_on("python", type=("build", "run"), when="+python")

    extends('python', when='+python')

    def cmake_args(self):
        args = [
            self.define_from_variant("WITH_PERL", "perl"),
            self.define_from_variant("WITH_PYTHON3", "python"),
            self.define("WITH_DOTNET", False),
            self.define("WITH_PYTHON2", False),
            self.define("WITH_VALA", False),
        ]
        if '+python' in self.spec:
            pynver = "python{0}".format(self.spec["python"].version.up_to(2))
            pysite = join_path(self.prefix.lib, pynver, "site-packages")
            args.append(self.define("PYTHON3_SITEPKG_DIR", pysite))
        return args
