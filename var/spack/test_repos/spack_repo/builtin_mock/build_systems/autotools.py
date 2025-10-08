# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import (
    BuilderWithDefaults,
    List,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    depends_on,
    register_builder,
    run_after,
)

from ._checks import execute_build_time_tests, execute_install_time_tests


class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools."""

    build_system_class = "AutotoolsPackage"
    default_buildsystem = "autotools"

    build_system("autotools")
    depends_on("gmake", type="build", when="build_system=autotools")

    def flags_to_build_system_args(self, flags):
        """Produces a list of all command line arguments to pass compiler flags to configure."""
        # Has to be dynamic attribute due to caching.
        configure_flag_args = []
        for flag, values in flags.items():
            if values:
                var_name = "LIBS" if flag == "ldlibs" else flag.upper()
                configure_flag_args.append(f"{var_name}={' '.join(values)}")
        # Spack's fflags are meant for both F77 and FC, therefore we additionally set FCFLAGS
        values = flags.get("fflags", None)
        if values:
            configure_flag_args.append(f"FCFLAGS={' '.join(values)}")
        setattr(self, "configure_flag_args", configure_flag_args)


@register_builder("autotools")
class AutotoolsBuilder(BuilderWithDefaults):
    #: Phases of a GNU Autotools package
    phases = ("autoreconf", "configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = ("configure_args", "check", "installcheck")

    #: Names associated with package attributes in the old build-system format
    package_attributes = (
        "archive_files",
        "build_time_test_callbacks",
        "install_time_test_callbacks",
        "configure_directory",
        "configure_abs_path",
        "build_directory",
    )

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    #: Callback names for install-time test
    install_time_test_callbacks = ["installcheck"]

    @property
    def archive_files(self) -> List[str]:
        return [os.path.join(self.build_directory, "config.log")]

    @property
    def configure_directory(self) -> str:
        """Return the directory where 'configure' resides."""
        return self.pkg.stage.source_path

    @property
    def configure_abs_path(self) -> str:
        # Absolute path to configure
        configure_abs_path = os.path.join(os.path.abspath(self.configure_directory), "configure")
        return configure_abs_path

    @property
    def build_directory(self) -> str:
        """Override to provide another place to build the package"""
        # Handle the case where the configure directory is set to a non-absolute path
        # Non-absolute paths are always relative to the staging source path
        build_dir = self.configure_directory
        if not os.path.isabs(build_dir):
            build_dir = os.path.join(self.pkg.stage.source_path, build_dir)
        return build_dir

    def configure_args(self) -> List[str]:
        """Return the list of all the arguments that must be passed to configure,
        except ``--prefix`` which will be pre-pended to the list.
        """
        return []

    def autoreconf(self, pkg: AutotoolsPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def configure(self, pkg: AutotoolsPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def build(self, pkg: AutotoolsPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def install(self, pkg: AutotoolsPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def check(self) -> None:
        pass

    run_after("build")(execute_build_time_tests)
    run_after("install")(execute_install_time_tests)
