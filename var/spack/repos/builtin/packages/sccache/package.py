# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import spack.build_systems
from spack.package import *


class Sccache(CargoPackage):
    """Sccache is a ccache-like tool. It is used as a compiler wrapper and avoids
    compilation when possible. Sccache has the capability to utilize caching in
    remote storage environments, including various cloud storage options, or
    alternatively, in local storage."""

    homepage = "https://github.com/mozilla/sccache"
    url = "https://github.com/mozilla/sccache/archive/refs/tags/v0.8.2.tar.gz"

    tags = ["build-tools"]

    executables = [r"^sccache$", r"^sscache-dist$"]

    license("Apache-2.0", checked_by="pranav-sivaraman")

    version("0.8.2", sha256="2b3e0ef8902fe7bcdcfccf393e29f4ccaafc0194cbb93681eaac238cdc9b94f8")
    version("0.8.1", sha256="30b951b49246d5ca7d614e5712215cb5f39509d6f899641f511fb19036b5c4e5")
    version("0.8.0", sha256="e78c7a65982e2ab1dc2e5580e548bb1bf6f47a0f20e58dcba8856fc97640f2d2")
    version("0.7.7", sha256="a5f5dacbc8232d566239fa023ce5fbc803ad56af2910fa1558b6e08e68e067e0")
    version("0.7.6", sha256="c6ff8750516fe982c9e9c20fb80d27c41481a22bf9a5a2346cff05724110bd42")
    version("0.7.5", sha256="19034b64ff223f852256869b3e3fa901059ee90de2e4085bf2bfb5690b430325")
    version("0.7.4", sha256="32301f125d5b1d73830b163fd15fe9b5c22cf4a4a6b835d893dec563aba5b4fc")
    version("0.7.3", sha256="7610667e53017f1d3e509e0be923608acfb85a6e77094b275e7b2db878aa3e3a")
    version("0.7.2", sha256="0ea726785ee694029848b1984a9c2571ce642ab25ec08c421ea88cc32c51eecd")
    version("0.7.1", sha256="5807417adbb120531ed5d7a18d5406e736be99b45ce9239ab196473fb405e62d")

    depends_on("rust@1.75:", when="@0.8.2:")
    depends_on("rust@1.70:", when="@0.7.7:")
    depends_on("rust@1.67.1:", when="@0.6:")
    depends_on("rust@1.65:", when="@0.4.2:")
    depends_on("rust@1.60:", when="@0.3.2:")
    depends_on("rust@1.58:", when="@0.3.1:")
    depends_on("pkgconfig", type="build", when="platform=linux")

    variant(
        "dist-server",
        default=False,
        description="Enables the sccache-dist binary",
        when="platform=linux",
    )

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"sccache (\S+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        if any(os.path.basename(path) == "sccache-dist" for path in exes):
            return "+dist-server"
        else:
            return "~dist-server"


class CargoBuilder(spack.build_systems.cargo.CargoBuilder):

    @property
    def build_args(self):
        if self.spec.satisfies("+dist-server"):
            return ["--features=dist-server"]

        return []
