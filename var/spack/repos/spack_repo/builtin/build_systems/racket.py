# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from typing import Optional, Tuple

from llnl.util.lang import ClassProperty, classproperty

from spack.build_environment import SPACK_NO_PARALLEL_MAKE
from spack.package import (
    Builder,
    Executable,
    PackageBase,
    Prefix,
    ProcessError,
    Spec,
    build_system,
    determine_number_of_jobs,
    extends,
    maintainers,
    register_builder,
    tty,
    working_dir,
)
from spack.util.environment import env_flag


def _homepage(cls: "RacketPackage") -> Optional[str]:
    if cls.racket_name:
        return f"https://pkgs.racket-lang.org/package/{cls.racket_name}"
    return None


class RacketPackage(PackageBase):
    """Specialized class for packages that are built using Racket's
    `raco pkg install` and `raco setup` commands.
    """

    #: Package name, version, and extension on PyPI
    maintainers("elfprince13")
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "RacketPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "racket"

    build_system("racket")

    extends("racket", when="build_system=racket")

    racket_name: Optional[str] = None
    homepage: ClassProperty[Optional[str]] = classproperty(_homepage)


@register_builder("racket")
class RacketBuilder(Builder):
    """The Racket builder provides an ``install`` phase that can be overridden."""

    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    legacy_methods: Tuple[str, ...] = tuple()

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ("build_directory", "build_time_test_callbacks", "subdirectory")

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    racket_name: Optional[str] = None

    @property
    def subdirectory(self):
        if self.pkg.racket_name:
            return "pkgs/{0}".format(self.pkg.racket_name)
        return None

    @property
    def build_directory(self):
        ret = os.getcwd()
        if self.subdirectory:
            ret = os.path.join(ret, self.subdirectory)
        return ret

    def install(self, pkg: RacketPackage, spec: Spec, prefix: Prefix) -> None:
        """Install everything from build directory."""
        raco = Executable("raco")
        with working_dir(self.build_directory):
            parallel = pkg.parallel and (not env_flag(SPACK_NO_PARALLEL_MAKE))
            name = pkg.racket_name
            assert name is not None, "Racket package name is not set"
            args = [
                "pkg",
                "install",
                "-t",
                "dir",
                "-n",
                name,
                "--deps",
                "fail",
                "--ignore-implies",
                "--copy",
                "-i",
                "-j",
                str(determine_number_of_jobs(parallel=parallel)),
                "--",
                os.getcwd(),
            ]
            try:
                raco(*args)
            except ProcessError:
                args.insert(-2, "--skip-installed")
                raco(*args)
                tty.warn(
                    f"Racket package {name} was already installed, uninstalling via "
                    "Spack may make someone unhappy!"
                )
