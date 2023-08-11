# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections.abc
import inspect
import os
import pathlib
import platform
import re
import sys
from typing import List, Optional, Tuple

import llnl.util.filesystem as fs

import spack.build_environment
import spack.builder
import spack.package_base
from spack.directives import build_system, conflicts, depends_on, variant
from spack.multimethod import when

from ._checks import BaseBuilder, execute_build_time_tests

# Regex to extract the primary generator from the CMake generator
# string.
_primary_generator_extractor = re.compile(r"(?:.* - )?(.*)")


def _extract_primary_generator(generator):
    """Use the compiled regex _primary_generator_extractor to extract the
    primary generator from the generator string which may contain an
    optional secondary generator.
    """
    primary_generator = _primary_generator_extractor.match(generator).group(1)
    return primary_generator


def generator(*names: str, default: Optional[str] = None):
    """The build system generator to use.

    See ``cmake --help`` for a list of valid generators.
    Currently, "Unix Makefiles" and "Ninja" are the only generators
    that Spack supports. Defaults to "Unix Makefiles".

    See https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html
    for more information.

    Args:
        names: allowed generators for this package
        default: default generator
    """
    allowed_values = ("make", "ninja")
    if any(x not in allowed_values for x in names):
        msg = "only 'make' and 'ninja' are allowed for CMake's 'generator' directive"
        raise ValueError(msg)

    default = default or names[0]
    not_used = [x for x in allowed_values if x not in names]

    def _values(x):
        return x in allowed_values

    _values.__doc__ = f"{','.join(names)}"

    variant(
        "generator",
        default=default,
        values=_values,
        description="the build system generator to use",
    )
    for x in not_used:
        conflicts(f"generator={x}")


class CMakePackage(spack.package_base.PackageBase):
    """Specialized class for packages built using CMake

    For more information on the CMake build system, see:
    https://cmake.org/cmake/help/latest/
    """

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "CMakePackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "cmake"

    build_system("cmake")

    with when("build_system=cmake"):
        # https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html
        # See https://github.com/spack/spack/pull/36679 and related issues for a
        # discussion of the trade-offs between Release and RelWithDebInfo for default
        # builds. Release is chosen to maximize performance and reduce disk-space burden,
        # at the cost of more difficulty in debugging.
        variant(
            "build_type",
            default="Release",
            description="CMake build type",
            values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
        )
        # CMAKE_INTERPROCEDURAL_OPTIMIZATION only exists for CMake >= 3.9
        # https://cmake.org/cmake/help/latest/variable/CMAKE_INTERPROCEDURAL_OPTIMIZATION.html
        variant(
            "ipo",
            default=False,
            when="^cmake@3.9:",
            description="CMake interprocedural optimization",
        )

        if sys.platform == "win32":
            generator("ninja")
        else:
            generator("ninja", "make", default="make")

        depends_on("cmake", type="build")
        depends_on("gmake", type="build", when="generator=make")
        depends_on("ninja", type="build", when="generator=ninja")

    def flags_to_build_system_args(self, flags):
        """Return a list of all command line arguments to pass the specified
        compiler flags to cmake. Note CMAKE does not have a cppflags option,
        so cppflags will be added to cflags, cxxflags, and fflags to mimic the
        behavior in other tools.
        """
        # Has to be dynamic attribute due to caching
        setattr(self, "cmake_flag_args", [])

        flag_string = "-DCMAKE_{0}_FLAGS={1}"
        langs = {"C": "c", "CXX": "cxx", "Fortran": "f"}

        # Handle language compiler flags
        for lang, pre in langs.items():
            flag = pre + "flags"
            # cmake has no explicit cppflags support -> add it to all langs
            lang_flags = " ".join(flags.get(flag, []) + flags.get("cppflags", []))
            if lang_flags:
                self.cmake_flag_args.append(flag_string.format(lang, lang_flags))

        # Cmake has different linker arguments for different build types.
        # We specify for each of them.
        if flags["ldflags"]:
            ldflags = " ".join(flags["ldflags"])
            ld_string = "-DCMAKE_{0}_LINKER_FLAGS={1}"
            # cmake has separate linker arguments for types of builds.
            for type in ["EXE", "MODULE", "SHARED", "STATIC"]:
                self.cmake_flag_args.append(ld_string.format(type, ldflags))

        # CMake has libs options separated by language. Apply ours to each.
        if flags["ldlibs"]:
            libs_flags = " ".join(flags["ldlibs"])
            libs_string = "-DCMAKE_{0}_STANDARD_LIBRARIES={1}"
            for lang in langs:
                self.cmake_flag_args.append(libs_string.format(lang, libs_flags))

    # Legacy methods (used by too many packages to change them,
    # need to forward to the builder)
    def define(self, *args, **kwargs):
        return self.builder.define(*args, **kwargs)

    def define_from_variant(self, *args, **kwargs):
        return self.builder.define_from_variant(*args, **kwargs)


@spack.builder.builder("cmake")
class CMakeBuilder(BaseBuilder):
    """The cmake builder encodes the default way of building software with CMake. IT
    has three phases that can be overridden:

        1. :py:meth:`~.CMakeBuilder.cmake`
        2. :py:meth:`~.CMakeBuilder.build`
        3. :py:meth:`~.CMakeBuilder.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.CMakeBuilder.cmake_args`.

    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:meth:`~.CMakeBuilder.root_cmakelists_dir` | Location of the    |
        |                                               | root CMakeLists.txt|
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.CMakeBuilder.build_directory`     | Directory where to |
        |                                               | build the package  |
        +-----------------------------------------------+--------------------+
    """

    #: Phases of a CMake package
    phases: Tuple[str, ...] = ("cmake", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods: Tuple[str, ...] = ("cmake_args", "check")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes: Tuple[str, ...] = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "archive_files",
        "root_cmakelists_dir",
        "std_cmake_args",
        "build_dirname",
        "build_directory",
    )

    #: Targets to be used during the build phase
    build_targets: List[str] = []
    #: Targets to be used during the install phase
    install_targets = ["install"]
    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    @property
    def archive_files(self):
        """Files to archive for packages based on CMake"""
        return [os.path.join(self.build_directory, "CMakeCache.txt")]

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.
        """
        return self.pkg.stage.source_path

    @property
    def generator(self):
        if self.spec.satisfies("generator=make"):
            return "Unix Makefiles"
        if self.spec.satisfies("generator=ninja"):
            return "Ninja"
        msg = f'{self.spec.format()} has an unsupported value for the "generator" variant'
        raise ValueError(msg)

    @property
    def std_cmake_args(self):
        """Standard cmake arguments provided as a property for
        convenience of package writers
        """
        std_cmake_args = CMakeBuilder.std_args(self.pkg, generator=self.generator)
        std_cmake_args += getattr(self.pkg, "cmake_flag_args", [])
        return std_cmake_args

    @staticmethod
    def std_args(pkg, generator=None):
        """Computes the standard cmake arguments for a generic package"""
        default_generator = "Ninja" if sys.platform == "win32" else "Unix Makefiles"
        generator = generator or default_generator
        valid_primary_generators = ["Unix Makefiles", "Ninja"]
        primary_generator = _extract_primary_generator(generator)
        if primary_generator not in valid_primary_generators:
            msg = "Invalid CMake generator: '{0}'\n".format(generator)
            msg += "CMakePackage currently supports the following "
            msg += "primary generators: '{0}'".format("', '".join(valid_primary_generators))
            raise spack.package_base.InstallError(msg)

        try:
            build_type = pkg.spec.variants["build_type"].value
        except KeyError:
            build_type = "RelWithDebInfo"

        try:
            ipo = pkg.spec.variants["ipo"].value
        except KeyError:
            ipo = False

        define = CMakeBuilder.define
        args = [
            "-G",
            generator,
            define("CMAKE_INSTALL_PREFIX", pathlib.Path(pkg.prefix).as_posix()),
            define("CMAKE_BUILD_TYPE", build_type),
            define("BUILD_TESTING", pkg.run_tests),
        ]

        # CMAKE_INTERPROCEDURAL_OPTIMIZATION only exists for CMake >= 3.9
        if pkg.spec.satisfies("^cmake@3.9:"):
            args.append(define("CMAKE_INTERPROCEDURAL_OPTIMIZATION", ipo))

        if primary_generator == "Unix Makefiles":
            args.append(define("CMAKE_VERBOSE_MAKEFILE", True))

        if platform.mac_ver()[0]:
            args.extend(
                [define("CMAKE_FIND_FRAMEWORK", "LAST"), define("CMAKE_FIND_APPBUNDLE", "LAST")]
            )

        # Set up CMake rpath
        args.extend(
            [
                define("CMAKE_INSTALL_RPATH_USE_LINK_PATH", True),
                define("CMAKE_INSTALL_RPATH", spack.build_environment.get_rpaths(pkg)),
                define("CMAKE_PREFIX_PATH", spack.build_environment.get_cmake_prefix_path(pkg)),
            ]
        )

        return args

    @staticmethod
    def define_cuda_architectures(pkg):
        """Returns the str ``-DCMAKE_CUDA_ARCHITECTURES:STRING=(expanded cuda_arch)``.

        ``cuda_arch`` is variant composed of a list of target CUDA architectures and
        it is declared in the cuda package.

        This method is no-op for cmake<3.18 and when ``cuda_arch`` variant is not set.

        """
        cmake_flag = str()
        if "cuda_arch" in pkg.spec.variants and pkg.spec.satisfies("^cmake@3.18:"):
            cmake_flag = CMakeBuilder.define(
                "CMAKE_CUDA_ARCHITECTURES", pkg.spec.variants["cuda_arch"].value
            )

        return cmake_flag

    @staticmethod
    def define_hip_architectures(pkg):
        """Returns the str ``-DCMAKE_HIP_ARCHITECTURES:STRING=(expanded amdgpu_target)``.

        ``amdgpu_target`` is variant composed of a list of the target HIP
        architectures and it is declared in the rocm package.

        This method is no-op for cmake<3.18 and when ``amdgpu_target`` variant is
        not set.

        """
        cmake_flag = str()
        if "amdgpu_target" in pkg.spec.variants and pkg.spec.satisfies("^cmake@3.21:"):
            cmake_flag = CMakeBuilder.define(
                "CMAKE_HIP_ARCHITECTURES", pkg.spec.variants["amdgpu_target"].value
            )

        return cmake_flag

    @staticmethod
    def define(cmake_var, value):
        """Return a CMake command line argument that defines a variable.

        The resulting argument will convert boolean values to OFF/ON
        and lists/tuples to CMake semicolon-separated string lists. All other
        values will be interpreted as strings.

        Examples:

            .. code-block:: python

                [define('BUILD_SHARED_LIBS', True),
                 define('CMAKE_CXX_STANDARD', 14),
                 define('swr', ['avx', 'avx2'])]

            will generate the following configuration options:

            .. code-block:: console

                ["-DBUILD_SHARED_LIBS:BOOL=ON",
                 "-DCMAKE_CXX_STANDARD:STRING=14",
                 "-DSWR:STRING=avx;avx2]

        """
        # Create a list of pairs. Each pair includes a configuration
        # option and whether or not that option is activated
        if isinstance(value, bool):
            kind = "BOOL"
            value = "ON" if value else "OFF"
        else:
            kind = "STRING"
            if isinstance(value, collections.abc.Sequence) and not isinstance(value, str):
                value = ";".join(str(v) for v in value)
            else:
                value = str(value)

        return "".join(["-D", cmake_var, ":", kind, "=", value])

    def define_from_variant(self, cmake_var, variant=None):
        """Return a CMake command line argument from the given variant's value.

        The optional ``variant`` argument defaults to the lower-case transform
        of ``cmake_var``.

        This utility function is similar to
        :meth:`~spack.build_systems.autotools.AutotoolsBuilder.with_or_without`.

        Examples:

            Given a package with:

            .. code-block:: python

                variant('cxxstd', default='11', values=('11', '14'),
                        multi=False, description='')
                variant('shared', default=True, description='')
                variant('swr', values=any_combination_of('avx', 'avx2'),
                        description='')

            calling this function like:

            .. code-block:: python

                [self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
                 self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
                 self.define_from_variant('SWR')]

            will generate the following configuration options:

            .. code-block:: console

                ["-DBUILD_SHARED_LIBS:BOOL=ON",
                 "-DCMAKE_CXX_STANDARD:STRING=14",
                 "-DSWR:STRING=avx;avx2]

            for ``<spec-name> cxxstd=14 +shared swr=avx,avx2``

        Note: if the provided variant is conditional, and the condition is not met,
                this function returns an empty string. CMake discards empty strings
                provided on the command line.
        """

        if variant is None:
            variant = cmake_var.lower()

        if variant not in self.pkg.variants:
            raise KeyError('"{0}" is not a variant of "{1}"'.format(variant, self.pkg.name))

        if variant not in self.pkg.spec.variants:
            return ""

        value = self.pkg.spec.variants[variant].value
        if isinstance(value, (tuple, list)):
            # Sort multi-valued variants for reproducibility
            value = sorted(value)

        return self.define(cmake_var, value)

    @property
    def build_dirname(self):
        """Directory name to use when building the package."""
        return "spack-build-%s" % self.pkg.spec.dag_hash(7)

    @property
    def build_directory(self):
        """Full-path to the directory to use when building the package."""
        return os.path.join(self.pkg.stage.path, self.build_dirname)

    def cmake_args(self):
        """List of all the arguments that must be passed to cmake, except:

            * CMAKE_INSTALL_PREFIX
            * CMAKE_BUILD_TYPE
            * BUILD_TESTING

        which will be set automatically.
        """
        return []

    def cmake(self, pkg, spec, prefix):
        """Runs ``cmake`` in the build directory"""
        options = self.std_cmake_args
        options += self.cmake_args()
        options.append(os.path.abspath(self.root_cmakelists_dir))
        with fs.working_dir(self.build_directory, create=True):
            inspect.getmodule(self.pkg).cmake(*options)

    def build(self, pkg, spec, prefix):
        """Make the build targets"""
        with fs.working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                inspect.getmodule(self.pkg).make(*self.build_targets)
            elif self.generator == "Ninja":
                self.build_targets.append("-v")
                inspect.getmodule(self.pkg).ninja(*self.build_targets)

    def install(self, pkg, spec, prefix):
        """Make the install targets"""
        with fs.working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                inspect.getmodule(self.pkg).make(*self.install_targets)
            elif self.generator == "Ninja":
                inspect.getmodule(self.pkg).ninja(*self.install_targets)

    spack.builder.run_after("build")(execute_build_time_tests)

    def check(self):
        """Search the CMake-generated files for the targets ``test`` and ``check``,
        and runs them if found.
        """
        with fs.working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                self.pkg._if_make_target_execute("test", jobs_env="CTEST_PARALLEL_LEVEL")
                self.pkg._if_make_target_execute("check")
            elif self.generator == "Ninja":
                self.pkg._if_ninja_target_execute("test", jobs_env="CTEST_PARALLEL_LEVEL")
                self.pkg._if_ninja_target_execute("check")
