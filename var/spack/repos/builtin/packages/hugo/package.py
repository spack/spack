# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hugo(Package):
    """The world's fastest framework for building websites."""

    homepage = "https://gohugo.io"
    url = "https://github.com/gohugoio/hugo/archive/v0.53.tar.gz"

    executables = ["^hugo$"]

    maintainers("alecbcs")

    version("0.111.1", sha256="a71d4e1f49ca7156d3811c0b10957816b75ff2e01b35ef326e7af94dfa554ec0")
    version("0.110.0", sha256="eeb137cefcea1a47ca27dc5f6573df29a8fe0b7f1ed0362faf7f73899e313770")
    version("0.109.0", sha256="35a5ba92057fe2c20b2218c374e762887021e978511d19bbe81ce4d9c21f0c78")
    version("0.108.0", sha256="dc90e9de22ce87c22063ce9c309cefacba89269a21eb369ed556b90b22b190c5")
    version("0.107.0", sha256="31d959a3c1633087d338147782d03bdef65323b67ff3efcec7b40241413e270a")
    version("0.106.0", sha256="9219434beb51466487b9f8518edcbc671027c1998e5a5820d76d517e1dfbd96a")

    # https://nvd.nist.gov/vuln/detail/CVE-2020-26284
    version(
        "0.74.3",
        sha256="9b296fa0396c20956fa6a1f7afadaa78739af62c277b6c0cfae79a91b0fe823f",
        deprecated=True,
    )
    version(
        "0.68.3",
        sha256="38e743605e45e3aafd9563feb9e78477e72d79535ce83b56b243ff991d3a2b6e",
        deprecated=True,
    )
    version(
        "0.53",
        sha256="48e65a33d3b10527101d13c354538379d9df698e5c38f60f4660386f4232e65c",
        deprecated=True,
    )

    # Uses go modules.
    # See https://gohugo.io/getting-started/installing/#fetch-from-github
    depends_on("go@1.11:", when="@0.48:", type="build")
    depends_on("go@1.18:", when="@0.106:", type="build")

    variant("extended", default=False, description="Enable extended features")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"Hugo Static Site Generator v(\S+)", output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        env.prepend_path("GOPATH", self.stage.path)

    def install(self, spec, prefix):
        go_args = ["build"]
        if self.spec.satisfies("+extended"):
            go_args.extend(["--tags", "extended"])

        go(*go_args)
        mkdirp(prefix.bin)
        install("hugo", prefix.bin)
