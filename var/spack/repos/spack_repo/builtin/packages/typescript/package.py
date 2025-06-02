# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Typescript(Package):
    """TypeScript is a superset of JavaScript that compiles to clean JavaScript output."""

    homepage = "https://www.typescriptlang.org"
    url = "https://github.com/microsoft/TypeScript/archive/refs/tags/v5.3.2.tar.gz"

    tags = ["build-tools"]

    license("Apache-2.0")

    version("5.8.3", sha256="d3ce895a57b59a41eba1053ee7c22c55261213d915a77f572fdb024f61f14a1e")
    version("5.3.2", sha256="c5a12507006e7d2b8020dec9589191ce070fd88203f2c80aca00d641cee7866f")

    depends_on("node-js@16:", type=("build", "link", "run"))
    depends_on("npm", type="build")

    executables = ["^tsc$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"Version\s+([\d.]+)\s*", output)
        return match.group(1) if match else None

    def install(self, spec, prefix):
        npm = which("npm", required=True)
        npm("install", "--global", f"--prefix={prefix}")
