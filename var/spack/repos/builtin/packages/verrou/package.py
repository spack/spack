# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import sys

from spack import *


class Verrou(AutotoolsPackage):
    """A floating-point error checker.

    Verrou helps you look for floating-point round-off errors in programs. It
    implements a stochastic floating-point arithmetic based on random rounding:
    all floating-point operations are perturbed by randomly switching rounding
    modes. This can be seen as an asynchronous variant of the CESTAC method, or
    a subset of Monte Carlo Arithmetic, performing only output randomization
    through random rounding.
    """

    homepage = "https://github.com/edf-hpc/verrou"
    url = "https://github.com/edf-hpc/verrou/archive/v2.0.0.tar.gz"
    git = "https://github.com/edf-hpc/verrou.git"

    maintainers = ["HadrienG2"]

    version("develop", branch="master")
    version(
        "2.2.0",
        sha256="d4ea3d19f0c61329723907b5b145d85776bb702643c1605a31f584484d2c5efc",
    )
    version(
        "2.1.0",
        sha256="b1ba49f84aebab15b8ab5649946c9c31b53ad1499f6ffb681c98db41ed28566d",
    )
    version(
        "2.0.0",
        sha256="798df6e426ec57646a2a626d756b72f0171647ae5b07c982952dae2d71e26045",
        deprecated=True,
    )
    version(
        "1.1.0",
        sha256="b5105f61c65680f31551199cd143b2e15f412c34c821537998a7165e315dde2d",
        deprecated=True,
    )

    # The server is sometimes a bit slow to respond
    timeout = {"timeout": 60}

    resource(
        name="valgrind-3.15.0",
        url="https://sourceware.org/pub/valgrind/valgrind-3.15.0.tar.bz2",
        sha256="417c7a9da8f60dd05698b3a7bc6002e4ef996f14c13f0ff96679a16873e78ab1",
        when="@2.2.0:",
        fetch_options=timeout,
    )
    resource(
        name="valgrind-3.14.0",
        url="https://sourceware.org/pub/valgrind/valgrind-3.14.0.tar.bz2",
        sha256="037c11bfefd477cc6e9ebe8f193bb237fe397f7ce791b4a4ce3fa1c6a520baa5",
        when="@2.1.0:2.1",
        fetch_options=timeout,
    )
    resource(
        name="valgrind-3.13.0",
        url="https://sourceware.org/pub/valgrind/valgrind-3.13.0.tar.bz2",
        sha256="d76680ef03f00cd5e970bbdcd4e57fb1f6df7d2e2c071635ef2be74790190c3b",
        when="@1.1.0:2.0",
        fetch_options=timeout,
    )

    variant(
        "fma",
        default=True,
        description="Activates fused multiply-add support for Verrou",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("python@:2", when="@1.1.0:2.0", type=("build", "run"))
    depends_on("python@3.0:", when="@2.1.0:", type=("build", "run"))
    extends("python")

    def patch(self):
        # We start with the verrou source tree and a "valgrind-x.y.z" subdir.
        # But we actually need a valgrind source tree with a "verrou" subdir.
        # First, let's locate the valgrind sources...
        valgrind_dirs = glob.glob("valgrind-*")
        assert len(valgrind_dirs) == 1
        valgrind_dir = valgrind_dirs[0]

        # ...then we can flip the directory organization around
        verrou_files = os.listdir(".")
        verrou_files.remove(valgrind_dir)
        os.mkdir("verrou")
        for name in verrou_files:
            os.rename(name, os.path.join("verrou", name))
        for name in os.listdir(valgrind_dir):
            os.rename(os.path.join(valgrind_dir, name), name)
        os.rmdir(valgrind_dir)

        # Once this is done, we can patch valgrind
        if self.spec.satisfies("@:2.0"):
            which("patch")("-p0", "--input=verrou/valgrind.diff")
        else:
            which("patch")("-p1", "--input=verrou/valgrind.diff")

        # Autogenerated perl path may be too long, need to fix this here
        # because these files are used during the build.
        for link_tool_in in glob.glob("coregrind/link_tool_exe_*.in"):
            filter_file("^#! @PERL@", "#! /usr/bin/env perl", link_tool_in)

    def autoreconf(self, spec, prefix):
        # Needed because we patched valgrind
        which("bash")("autogen.sh")

    def configure_args(self):
        spec = self.spec
        options = [
            "--enable-only64bit",
            "--{0}able-verrou-fma".format("en" if "+fma" in spec else "dis"),
        ]

        if sys.platform == "darwin":
            options.append("--build=amd64-darwin")

        return options
