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
    Tuple,
    build_system,
    depends_on,
    register_builder,
    run_after,
)

from ._checks import execute_build_time_tests


class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake

    For more information on the CMake build system, see:
    https://cmake.org/cmake/help/latest/
    """

    build_system_class = "CMakePackage"
    default_buildsystem = "cmake"

    build_system("cmake")
    depends_on("cmake", type="build", when="build_system=cmake")

    def flags_to_build_system_args(self, flags):
        """Translate compiler flags to CMake arguments."""
        # Has to be dynamic attribute due to caching
        cmake_flag_args = []

        for lang, pre in (("C", "c"), ("CXX", "cxx"), ("Fortran", "f")):
            lang_flags = " ".join(flags.get(f"{pre}flags", []) + flags.get("cppflags", []))
            if lang_flags:
                cmake_flag_args.append(f"-DCMAKE_{lang}_FLAGS={lang_flags}")

        if flags["ldflags"]:
            ldflags = " ".join(flags["ldflags"])
            cmake_flag_args.append(f"-DCMAKE_EXE_LINKER_FLAGS={ldflags}")
            cmake_flag_args.append(f"-DCMAKE_MODULE_LINKER_FLAGS={ldflags}")
            cmake_flag_args.append(f"-DCMAKE_SHARED_LINKER_FLAGS={ldflags}")

        if flags["ldlibs"]:
            libs_flags = " ".join(flags["ldlibs"])
            for lang in ("C", "CXX", "Fortran"):
                cmake_flag_args.append(f"-DCMAKE_{lang}_STANDARD_LIBRARIES={libs_flags}")

        setattr(self, "cmake_flag_args", cmake_flag_args)


@register_builder("cmake")
class CMakeBuilder(BuilderWithDefaults):
    """Builder for CMake packages"""

    #: Phases of a CMake package
    phases: Tuple[str, ...] = ("cmake", "build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods: Tuple[str, ...] = ("cmake_args", "check")

    #: Names associated with package attributes in the old build-system format
    package_attributes: Tuple[str, ...] = (
        "build_time_test_callbacks",
        "archive_files",
        "build_directory",
    )

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    @property
    def archive_files(self) -> List[str]:
        return [os.path.join(self.build_directory, "CMakeCache.txt")]

    @property
    def build_directory(self) -> str:
        return os.path.join(self.pkg.stage.path, "build")

    def cmake_args(self) -> List[str]:
        return []

    def cmake(self, pkg: CMakePackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def build(self, pkg: CMakePackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def install(self, pkg: CMakePackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def check(self) -> None:
        pass

    run_after("build")(execute_build_time_tests)
