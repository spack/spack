# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.build_environment import MakeExecutable, determine_number_of_jobs
from spack.package import *


class Gmake(AutotoolsPackage, GNUMirrorPackage):
    """GNU Make is a tool which controls the generation of executables and
    other non-source files of a program from the program's source files."""

    homepage = "https://www.gnu.org/software/make/"
    gnu_mirror_path = "make/make-4.2.1.tar.gz"
    maintainers("haampie")

    # Stable releases
    version("4.4", sha256="581f4d4e872da74b3941c874215898a7d35802f03732bdccee1d4a7979105d18")
    version("4.3", sha256="e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19")
    version("4.2.1", sha256="e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7")
    version("4.0", sha256="fc42139fb0d4b4291929788ebaf77e2a4de7eaca95e31f3634ef7d4932051f69")

    variant("guile", default=False, description="Support GNU Guile for embedded scripting")

    with when("+guile"):
        depends_on("guile@:2.0", when="@:4.2")
        depends_on("guile@:3.0")
        depends_on("pkgconfig", type="build")

    # build.sh requires it in 4.0 (SV 40254)
    conflicts("~guile", when="@4.0")

    patch(
        "https://src.fedoraproject.org/rpms/make/raw/519a7c5bcbead22e6ea2d2c2341d981ef9e25c0d/f/make-4.2.1-glob-fix-2.patch",
        level=1,
        sha256="fe5b60d091c33f169740df8cb718bf4259f84528b42435194ffe0dd5b79cd125",
        when="@4.2.1",
    )
    patch(
        "https://src.fedoraproject.org/rpms/make/raw/519a7c5bcbead22e6ea2d2c2341d981ef9e25c0d/f/make-4.2.1-glob-fix-3.patch",
        level=1,
        sha256="ca60bd9c1a1b35bc0dc58b6a4a19d5c2651f7a94a4b22b2c5ea001a1ca7a8a7f",
        when="@:4.2.1",
    )

    # Avoid symlinking GNUMakefile to GNUMakefile
    build_directory = "spack-build"

    # See https://savannah.gnu.org/bugs/?57962
    patch("findprog-in-ignore-directories.patch", when="@4.3")

    tags = ["build-tools"]

    executables = ["^g?make$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU Make (\S+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        args = []
        args.extend(self.with_or_without("guile"))
        args.append("--disable-nls")
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            Executable(os.path.join(os.curdir, "build.sh"))()

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            os.mkdir(prefix.bin)
            install("make", prefix.bin)
            os.symlink("make", prefix.bin.gmake)

    def setup_dependent_package(self, module, dspec):
        module.make = MakeExecutable(
            self.spec.prefix.bin.make, determine_number_of_jobs(parallel=dspec.package.parallel)
        )
        module.gmake = MakeExecutable(
            self.spec.prefix.bin.gmake, determine_number_of_jobs(parallel=dspec.package.parallel)
        )
