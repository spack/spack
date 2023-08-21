# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module contains all routines related to setting up the package
build environment.  All of this is set up by package.py just before
install() is called.

There are two parts to the build environment:

1. Python build environment (i.e. install() method)

   This is how things are set up when install() is called.  Spack
   takes advantage of each package being in its own module by adding a
   bunch of command-like functions (like configure(), make(), etc.) in
   the package's module scope.  Ths allows package writers to call
   them all directly in Package.install() without writing 'self.'
   everywhere.  No, this isn't Pythonic.  Yes, it makes the code more
   readable and more like the shell script from which someone is
   likely porting.

2. Build execution environment

   This is the set of environment variables, like PATH, CC, CXX,
   etc. that control the build.  There are also a number of
   environment variables used to pass information (like RPATHs and
   other information about dependencies) to Spack's compiler wrappers.
   All of these env vars are also set up here.

Skimming this module is a nice way to get acquainted with the types of
calls you can make from within the install() function.
"""
import inspect
import io
import multiprocessing
import os
import re
import sys
import traceback
import types
from typing import List, Tuple

import llnl.util.tty as tty
from llnl.util.filesystem import join_path
from llnl.util.lang import dedupe
from llnl.util.symlink import symlink
from llnl.util.tty.color import cescape, colorize
from llnl.util.tty.log import MultiProcessFd

import spack.build_systems.cmake
import spack.build_systems.meson
import spack.build_systems.python
import spack.builder
import spack.config
import spack.main
import spack.package_base
import spack.paths
import spack.platforms
import spack.repo
import spack.schema.environment
import spack.store
import spack.subprocess_context
import spack.user_environment
import spack.util.path
import spack.util.pattern
from spack.error import NoHeadersError, NoLibrariesError
from spack.install_test import spack_install_test_log
from spack.installer import InstallError
from spack.util.cpus import cpus_available
from spack.util.environment import (
    SYSTEM_DIRS,
    EnvironmentModifications,
    env_flag,
    filter_system_paths,
    get_path,
    inspect_path,
    is_system_path,
    validate,
)
from spack.util.executable import Executable
from spack.util.log_parse import make_log_context, parse_log_events
from spack.util.module_cmd import load_module, module, path_from_modules
from spack.util.string import plural

#
# This can be set by the user to globally disable parallel builds.
#
SPACK_NO_PARALLEL_MAKE = "SPACK_NO_PARALLEL_MAKE"

#
# These environment variables are set by
# set_wrapper_variables and used to pass parameters to
# Spack's compiler wrappers.
#
SPACK_ENV_PATH = "SPACK_ENV_PATH"
SPACK_INCLUDE_DIRS = "SPACK_INCLUDE_DIRS"
SPACK_LINK_DIRS = "SPACK_LINK_DIRS"
SPACK_RPATH_DIRS = "SPACK_RPATH_DIRS"
SPACK_RPATH_DEPS = "SPACK_RPATH_DEPS"
SPACK_LINK_DEPS = "SPACK_LINK_DEPS"
SPACK_PREFIX = "SPACK_PREFIX"
SPACK_INSTALL = "SPACK_INSTALL"
SPACK_DEBUG = "SPACK_DEBUG"
SPACK_SHORT_SPEC = "SPACK_SHORT_SPEC"
SPACK_DEBUG_LOG_ID = "SPACK_DEBUG_LOG_ID"
SPACK_DEBUG_LOG_DIR = "SPACK_DEBUG_LOG_DIR"
SPACK_CCACHE_BINARY = "SPACK_CCACHE_BINARY"
SPACK_SYSTEM_DIRS = "SPACK_SYSTEM_DIRS"


# Platform-specific library suffix.
if sys.platform == "darwin":
    dso_suffix = "dylib"
elif sys.platform == "win32":
    dso_suffix = "dll"
else:
    dso_suffix = "so"

stat_suffix = "lib" if sys.platform == "win32" else "a"


def jobserver_enabled():
    """Returns true if a posix jobserver (make) is detected."""
    return "MAKEFLAGS" in os.environ and "--jobserver" in os.environ["MAKEFLAGS"]


def get_effective_jobs(jobs, parallel=True, supports_jobserver=False):
    """Return the number of jobs, or None if supports_jobserver and a jobserver is detected."""
    if not parallel or jobs <= 1 or env_flag(SPACK_NO_PARALLEL_MAKE):
        return 1
    if supports_jobserver and jobserver_enabled():
        return None
    return jobs


class MakeExecutable(Executable):
    """Special callable executable object for make so the user can specify
    parallelism options on a per-invocation basis.  Specifying
    'parallel' to the call will override whatever the package's
    global setting is, so you can either default to true or false and
    override particular calls. Specifying 'jobs_env' to a particular
    call will name an environment variable which will be set to the
    parallelism level (without affecting the normal invocation with
    -j).
    """

    def __init__(self, name, jobs, **kwargs):
        supports_jobserver = kwargs.pop("supports_jobserver", True)
        super().__init__(name, **kwargs)
        self.supports_jobserver = supports_jobserver
        self.jobs = jobs

    def __call__(self, *args, **kwargs):
        """parallel, and jobs_env from kwargs are swallowed and used here;
        remaining arguments are passed through to the superclass.
        """
        parallel = kwargs.pop("parallel", True)
        jobs_env = kwargs.pop("jobs_env", None)
        jobs_env_supports_jobserver = kwargs.pop("jobs_env_supports_jobserver", False)

        jobs = get_effective_jobs(
            self.jobs, parallel=parallel, supports_jobserver=self.supports_jobserver
        )
        if jobs is not None:
            args = ("-j{0}".format(jobs),) + args

        if jobs_env:
            # Caller wants us to set an environment variable to
            # control the parallelism.
            jobs_env_jobs = get_effective_jobs(
                self.jobs, parallel=parallel, supports_jobserver=jobs_env_supports_jobserver
            )
            if jobs_env_jobs is not None:
                kwargs["extra_env"] = {jobs_env: str(jobs_env_jobs)}

        return super().__call__(*args, **kwargs)


def _on_cray():
    host_platform = spack.platforms.host()
    host_os = host_platform.operating_system("default_os")
    on_cray = str(host_platform) == "cray"
    using_cnl = re.match(r"cnl\d+", str(host_os))
    return on_cray, using_cnl


def clean_environment():
    # Stuff in here sanitizes the build environment to eliminate
    # anything the user has set that may interfere. We apply it immediately
    # unlike the other functions so it doesn't overwrite what the modules load.
    env = EnvironmentModifications()

    # Remove these vars from the environment during build because they
    # can affect how some packages find libraries.  We want to make
    # sure that builds never pull in unintended external dependencies.
    env.unset("LD_LIBRARY_PATH")
    env.unset("LD_RUN_PATH")
    env.unset("DYLD_LIBRARY_PATH")
    env.unset("DYLD_FALLBACK_LIBRARY_PATH")

    # These vars affect how the compiler finds libraries and include dirs.
    env.unset("LIBRARY_PATH")
    env.unset("CPATH")
    env.unset("C_INCLUDE_PATH")
    env.unset("CPLUS_INCLUDE_PATH")
    env.unset("OBJC_INCLUDE_PATH")

    env.unset("CMAKE_PREFIX_PATH")
    env.unset("PYTHONPATH")
    env.unset("R_HOME")
    env.unset("R_ENVIRON")

    # Affects GNU make, can e.g. indirectly inhibit enabling parallel build
    # env.unset('MAKEFLAGS')

    # Avoid that libraries of build dependencies get hijacked.
    env.unset("LD_PRELOAD")
    env.unset("DYLD_INSERT_LIBRARIES")

    # Avoid <packagename>_ROOT user variables overriding spack dependencies
    # https://cmake.org/cmake/help/latest/variable/PackageName_ROOT.html
    # Spack needs SPACK_ROOT though, so we need to exclude that
    for varname in os.environ.keys():
        if varname.endswith("_ROOT") and varname != "SPACK_ROOT":
            env.unset(varname)

    # On Cray "cluster" systems, unset CRAY_LD_LIBRARY_PATH to avoid
    # interference with Spack dependencies.
    # CNL requires these variables to be set (or at least some of them,
    # depending on the CNL version).
    on_cray, using_cnl = _on_cray()
    if on_cray and not using_cnl:
        env.unset("CRAY_LD_LIBRARY_PATH")
        for varname in os.environ.keys():
            if "PKGCONF" in varname:
                env.unset(varname)

    # Unset the following variables because they can affect installation of
    # Autotools and CMake packages.
    build_system_vars = [
        "CC",
        "CFLAGS",
        "CPP",
        "CPPFLAGS",  # C variables
        "CXX",
        "CCC",
        "CXXFLAGS",
        "CXXCPP",  # C++ variables
        "F77",
        "FFLAGS",
        "FLIBS",  # Fortran77 variables
        "FC",
        "FCFLAGS",
        "FCLIBS",  # Fortran variables
        "LDFLAGS",
        "LIBS",  # linker variables
    ]
    for v in build_system_vars:
        env.unset(v)

    # Unset mpi environment vars. These flags should only be set by
    # mpi providers for packages with mpi dependencies
    mpi_vars = ["MPICC", "MPICXX", "MPIFC", "MPIF77", "MPIF90"]
    for v in mpi_vars:
        env.unset(v)

    build_lang = spack.config.get("config:build_language")
    if build_lang:
        # Override language-related variables. This can be used to force
        # English compiler messages etc., which allows parse_log_events to
        # show useful matches.
        env.set("LC_ALL", build_lang)

    # Remove any macports installs from the PATH.  The macports ld can
    # cause conflicts with the built-in linker on el capitan.  Solves
    # assembler issues, e.g.:
    #    suffix or operands invalid for `movq'"
    path = get_path("PATH")
    for p in path:
        if "/macports/" in p:
            env.remove_path("PATH", p)

    return env


def _add_werror_handling(keep_werror, env):
    keep_flags = set()
    # set of pairs
    replace_flags: List[Tuple[str, str]] = []
    if keep_werror == "all":
        keep_flags.add("-Werror*")
    else:
        if keep_werror == "specific":
            keep_flags.add("-Werror-*")
            keep_flags.add("-Werror=*")
        # This extra case is to handle -Werror-implicit-function-declaration
        replace_flags.append(("-Werror-", "-Wno-error="))
        replace_flags.append(("-Werror", "-Wno-error"))
    env.set("SPACK_COMPILER_FLAGS_KEEP", "|".join(keep_flags))
    env.set("SPACK_COMPILER_FLAGS_REPLACE", " ".join(["|".join(item) for item in replace_flags]))


def set_compiler_environment_variables(pkg, env):
    assert pkg.spec.concrete
    compiler = pkg.compiler
    spec = pkg.spec

    # Make sure the executables for this compiler exist
    compiler.verify_executables()

    # Set compiler variables used by CMake and autotools
    assert all(key in compiler.link_paths for key in ("cc", "cxx", "f77", "fc"))

    # Populate an object with the list of environment modifications
    # and return it
    # TODO : add additional kwargs for better diagnostics, like requestor,
    # ttyout, ttyerr, etc.
    link_dir = spack.paths.build_env_path

    # Set SPACK compiler variables so that our wrapper knows what to call
    if compiler.cc:
        env.set("SPACK_CC", compiler.cc)
        env.set("CC", os.path.join(link_dir, compiler.link_paths["cc"]))
    if compiler.cxx:
        env.set("SPACK_CXX", compiler.cxx)
        env.set("CXX", os.path.join(link_dir, compiler.link_paths["cxx"]))
    if compiler.f77:
        env.set("SPACK_F77", compiler.f77)
        env.set("F77", os.path.join(link_dir, compiler.link_paths["f77"]))
    if compiler.fc:
        env.set("SPACK_FC", compiler.fc)
        env.set("FC", os.path.join(link_dir, compiler.link_paths["fc"]))

    # Set SPACK compiler rpath flags so that our wrapper knows what to use
    env.set("SPACK_CC_RPATH_ARG", compiler.cc_rpath_arg)
    env.set("SPACK_CXX_RPATH_ARG", compiler.cxx_rpath_arg)
    env.set("SPACK_F77_RPATH_ARG", compiler.f77_rpath_arg)
    env.set("SPACK_FC_RPATH_ARG", compiler.fc_rpath_arg)
    env.set("SPACK_LINKER_ARG", compiler.linker_arg)

    # Check whether we want to force RPATH or RUNPATH
    if spack.config.get("config:shared_linking:type") == "rpath":
        env.set("SPACK_DTAGS_TO_STRIP", compiler.enable_new_dtags)
        env.set("SPACK_DTAGS_TO_ADD", compiler.disable_new_dtags)
    else:
        env.set("SPACK_DTAGS_TO_STRIP", compiler.disable_new_dtags)
        env.set("SPACK_DTAGS_TO_ADD", compiler.enable_new_dtags)

    if pkg.keep_werror is not None:
        keep_werror = pkg.keep_werror
    else:
        keep_werror = spack.config.get("config:flags:keep_werror")

    _add_werror_handling(keep_werror, env)

    # Set the target parameters that the compiler will add
    # Don't set on cray platform because the targeting module handles this
    if spec.satisfies("platform=cray"):
        isa_arg = ""
    else:
        isa_arg = spec.architecture.target.optimization_flags(compiler)
    env.set("SPACK_TARGET_ARGS", isa_arg)

    # Trap spack-tracked compiler flags as appropriate.
    # env_flags are easy to accidentally override.
    inject_flags = {}
    env_flags = {}
    build_system_flags = {}
    for flag in spack.spec.FlagMap.valid_compiler_flags():
        # Always convert flag_handler to function type.
        # This avoids discrepencies in calling conventions between functions
        # and methods, or between bound and unbound methods in python 2.
        # We cannot effectively convert everything to a bound method, which
        # would be the simpler solution.
        if isinstance(pkg.flag_handler, types.FunctionType):
            handler = pkg.flag_handler
        else:
            handler = pkg.flag_handler.__func__

        injf, envf, bsf = handler(pkg, flag, spec.compiler_flags[flag][:])
        inject_flags[flag] = injf or []
        env_flags[flag] = envf or []
        build_system_flags[flag] = bsf or []

    # Place compiler flags as specified by flag_handler
    for flag in spack.spec.FlagMap.valid_compiler_flags():
        # Concreteness guarantees key safety here
        if inject_flags[flag]:
            # variables SPACK_<FLAG> inject flags through wrapper
            var_name = "SPACK_{0}".format(flag.upper())
            env.set(var_name, " ".join(f for f in inject_flags[flag]))
        if env_flags[flag]:
            # implicit variables
            env.set(flag.upper(), " ".join(f for f in env_flags[flag]))
    pkg.flags_to_build_system_args(build_system_flags)

    env.set("SPACK_COMPILER_SPEC", str(spec.compiler))

    env.set("SPACK_SYSTEM_DIRS", ":".join(SYSTEM_DIRS))

    compiler.setup_custom_environment(pkg, env)

    return env


def set_wrapper_variables(pkg, env):
    """Set environment variables used by the Spack compiler wrapper
    (which have the prefix `SPACK_`) and also add the compiler wrappers
    to PATH.

    This determines the injected -L/-I/-rpath options; each
    of these specifies a search order and this function computes these
    options in a manner that is intended to match the DAG traversal order
    in `modifications_from_dependencies`: that method uses a post-order
    traversal so that `PrependPath` actions from dependencies take lower
    precedence; we use a post-order traversal here to match the visitation
    order of `modifications_from_dependencies` (so we are visiting the
    lowest priority packages first).
    """
    # Set environment variables if specified for
    # the given compiler
    compiler = pkg.compiler
    env.extend(spack.schema.environment.parse(compiler.environment))

    if compiler.extra_rpaths:
        extra_rpaths = ":".join(compiler.extra_rpaths)
        env.set("SPACK_COMPILER_EXTRA_RPATHS", extra_rpaths)

    # Add spack build environment path with compiler wrappers first in
    # the path. We add the compiler wrapper path, which includes default
    # wrappers (cc, c++, f77, f90), AND a subdirectory containing
    # compiler-specific symlinks.  The latter ensures that builds that
    # are sensitive to the *name* of the compiler see the right name when
    # we're building with the wrappers.
    #
    # Conflicts on case-insensitive systems (like "CC" and "cc") are
    # handled by putting one in the <build_env_path>/case-insensitive
    # directory.  Add that to the path too.
    env_paths = []
    compiler_specific = os.path.join(
        spack.paths.build_env_path, os.path.dirname(pkg.compiler.link_paths["cc"])
    )
    for item in [spack.paths.build_env_path, compiler_specific]:
        env_paths.append(item)
        ci = os.path.join(item, "case-insensitive")
        if os.path.isdir(ci):
            env_paths.append(ci)

    tty.debug("Adding compiler bin/ paths: " + " ".join(env_paths))
    for item in env_paths:
        env.prepend_path("PATH", item)
    env.set_path(SPACK_ENV_PATH, env_paths)

    # Working directory for the spack command itself, for debug logs.
    if spack.config.get("config:debug"):
        env.set(SPACK_DEBUG, "TRUE")
    env.set(SPACK_SHORT_SPEC, pkg.spec.short_spec)
    env.set(SPACK_DEBUG_LOG_ID, pkg.spec.format("{name}-{hash:7}"))
    env.set(SPACK_DEBUG_LOG_DIR, spack.main.spack_working_dir)

    # Find ccache binary and hand it to build environment
    if spack.config.get("config:ccache"):
        ccache = Executable("ccache")
        if not ccache:
            raise RuntimeError("No ccache binary found in PATH")
        env.set(SPACK_CCACHE_BINARY, ccache)

    # Gather information about various types of dependencies
    link_deps = set(pkg.spec.traverse(root=False, deptype=("link")))
    rpath_deps = get_rpath_deps(pkg)

    link_dirs = []
    include_dirs = []
    rpath_dirs = []

    def _prepend_all(list_to_modify, items_to_add):
        # Update the original list (creating a new list would be faster but
        # may not be convenient)
        for item in reversed(list(items_to_add)):
            list_to_modify.insert(0, item)

    def update_compiler_args_for_dep(dep):
        if dep in link_deps and (not is_system_path(dep.prefix)):
            query = pkg.spec[dep.name]
            dep_link_dirs = list()
            try:
                # In some circumstances (particularly for externals) finding
                # libraries packages can be time consuming, so indicate that
                # we are performing this operation (and also report when it
                # finishes).
                tty.debug("Collecting libraries for {0}".format(dep.name))
                dep_link_dirs.extend(query.libs.directories)
                tty.debug("Libraries for {0} have been collected.".format(dep.name))
            except NoLibrariesError:
                tty.debug("No libraries found for {0}".format(dep.name))

            for default_lib_dir in ["lib", "lib64"]:
                default_lib_prefix = os.path.join(dep.prefix, default_lib_dir)
                if os.path.isdir(default_lib_prefix):
                    dep_link_dirs.append(default_lib_prefix)

            _prepend_all(link_dirs, dep_link_dirs)
            if dep in rpath_deps:
                _prepend_all(rpath_dirs, dep_link_dirs)

            try:
                _prepend_all(include_dirs, query.headers.directories)
            except NoHeadersError:
                tty.debug("No headers found for {0}".format(dep.name))

    for dspec in pkg.spec.traverse(root=False, order="post"):
        if dspec.external:
            update_compiler_args_for_dep(dspec)

    # Just above, we prepended entries for -L/-rpath for externals. We
    # now do this for non-external packages so that Spack-built packages
    # are searched first for libraries etc.
    for dspec in pkg.spec.traverse(root=False, order="post"):
        if not dspec.external:
            update_compiler_args_for_dep(dspec)

    # The top-level package is always RPATHed. It hasn't been installed yet
    # so the RPATHs are added unconditionally (e.g. even though lib64/ may
    # not be created for the install).
    for libdir in ["lib64", "lib"]:
        lib_path = os.path.join(pkg.prefix, libdir)
        rpath_dirs.insert(0, lib_path)

    link_dirs = list(dedupe(filter_system_paths(link_dirs)))
    include_dirs = list(dedupe(filter_system_paths(include_dirs)))
    rpath_dirs = list(dedupe(filter_system_paths(rpath_dirs)))

    env.set(SPACK_LINK_DIRS, ":".join(link_dirs))
    env.set(SPACK_INCLUDE_DIRS, ":".join(include_dirs))
    env.set(SPACK_RPATH_DIRS, ":".join(rpath_dirs))


def determine_number_of_jobs(
    parallel=False, command_line=None, config_default=None, max_cpus=None
):
    """
    Packages that require sequential builds need 1 job. Otherwise we use the
    number of jobs set on the command line. If not set, then we use the config
    defaults (which is usually set through the builtin config scope), but we
    cap to the number of CPUs available to avoid oversubscription.

    Parameters:
        parallel (bool or None): true when package supports parallel builds
        command_line (int or None): command line override
        config_default (int or None): config default number of jobs
        max_cpus (int or None): maximum number of CPUs available. When None, this
            value is automatically determined.
    """
    if not parallel:
        return 1

    if command_line is None and "command_line" in spack.config.scopes():
        command_line = spack.config.get("config:build_jobs", scope="command_line")

    if command_line is not None:
        return command_line

    max_cpus = max_cpus or cpus_available()

    # in some rare cases _builtin config may not be set, so default to max 16
    config_default = config_default or spack.config.get("config:build_jobs", 16)

    return min(max_cpus, config_default)


def set_module_variables_for_package(pkg):
    """Populate the Python module of a package with some useful global names.
    This makes things easier for package writers.
    """
    # Put a marker on this module so that it won't execute the body of this
    # function again, since it is not needed
    marker = "_set_run_already_called"
    if getattr(pkg.module, marker, False):
        return

    module = ModuleChangePropagator(pkg)

    jobs = determine_number_of_jobs(parallel=pkg.parallel)

    m = module
    m.make_jobs = jobs

    # TODO: make these build deps that can be installed if not found.
    m.make = MakeExecutable("make", jobs)
    m.ninja = MakeExecutable("ninja", jobs, supports_jobserver=False)
    # TODO: johnwparent: add package or builder support to define these build tools
    # for now there is no entrypoint for builders to define these on their
    # own
    if sys.platform == "win32":
        m.nmake = Executable("nmake")
        m.msbuild = Executable("msbuild")
        # analog to configure for win32
        m.cscript = Executable("cscript")

    # Find the configure script in the archive path
    # Don't use which for this; we want to find it in the current dir.
    m.configure = Executable("./configure")

    # Standard CMake arguments
    m.std_cmake_args = spack.build_systems.cmake.CMakeBuilder.std_args(pkg)
    m.std_meson_args = spack.build_systems.meson.MesonBuilder.std_args(pkg)
    m.std_pip_args = spack.build_systems.python.PythonPipBuilder.std_args(pkg)

    # Put spack compiler paths in module scope.
    link_dir = spack.paths.build_env_path
    m.spack_cc = os.path.join(link_dir, pkg.compiler.link_paths["cc"])
    m.spack_cxx = os.path.join(link_dir, pkg.compiler.link_paths["cxx"])
    m.spack_f77 = os.path.join(link_dir, pkg.compiler.link_paths["f77"])
    m.spack_fc = os.path.join(link_dir, pkg.compiler.link_paths["fc"])

    # Useful directories within the prefix are encapsulated in
    # a Prefix object.
    m.prefix = pkg.prefix

    # Platform-specific library suffix.
    m.dso_suffix = dso_suffix

    def static_to_shared_library(static_lib, shared_lib=None, **kwargs):
        compiler_path = kwargs.get("compiler", m.spack_cc)
        compiler = Executable(compiler_path)

        return _static_to_shared_library(
            pkg.spec.architecture, compiler, static_lib, shared_lib, **kwargs
        )

    m.static_to_shared_library = static_to_shared_library

    # Put a marker on this module so that it won't execute the body of this
    # function again, since it is not needed
    setattr(m, marker, True)
    module.propagate_changes_to_mro()


def _static_to_shared_library(arch, compiler, static_lib, shared_lib=None, **kwargs):
    """
    Converts a static library to a shared library. The static library has to
    be built with PIC for the conversion to work.

    Parameters:
        static_lib (str): Path to the static library.
        shared_lib (str): Path to the shared library. Default is to derive
                          from the static library's path.

    Keyword arguments:
        compiler (str): Path to the compiler. Default is spack_cc.
        compiler_output: Where to print compiler output to.
        arguments (str list): Additional arguments for the compiler.
        version (str): Library version. Default is unspecified.
        compat_version (str): Library compatibility version. Default is
                              version.
    """
    compiler_output = kwargs.get("compiler_output", None)
    arguments = kwargs.get("arguments", [])
    version = kwargs.get("version", None)
    compat_version = kwargs.get("compat_version", version)

    if not shared_lib:
        shared_lib = "{0}.{1}".format(os.path.splitext(static_lib)[0], dso_suffix)

    compiler_args = []

    # TODO: Compiler arguments should not be hardcoded but provided by
    #       the different compiler classes.
    if "linux" in arch or "cray" in arch:
        soname = os.path.basename(shared_lib)

        if compat_version:
            soname += ".{0}".format(compat_version)

        compiler_args = [
            "-shared",
            "-Wl,-soname,{0}".format(soname),
            "-Wl,--whole-archive",
            static_lib,
            "-Wl,--no-whole-archive",
        ]
    elif "darwin" in arch:
        install_name = shared_lib

        if compat_version:
            install_name += ".{0}".format(compat_version)

        compiler_args = [
            "-dynamiclib",
            "-install_name",
            "{0}".format(install_name),
            "-Wl,-force_load,{0}".format(static_lib),
        ]

        if compat_version:
            compiler_args.extend(["-compatibility_version", "{0}".format(compat_version)])

        if version:
            compiler_args.extend(["-current_version", "{0}".format(version)])

    if len(arguments) > 0:
        compiler_args.extend(arguments)

    shared_lib_base = shared_lib

    if version:
        shared_lib += ".{0}".format(version)
    elif compat_version:
        shared_lib += ".{0}".format(compat_version)

    compiler_args.extend(["-o", shared_lib])

    # Create symlinks for version and compat_version
    shared_lib_link = os.path.basename(shared_lib)

    if version or compat_version:
        symlink(shared_lib_link, shared_lib_base)

    if compat_version and compat_version != version:
        symlink(shared_lib_link, "{0}.{1}".format(shared_lib_base, compat_version))

    return compiler(*compiler_args, output=compiler_output)


def get_rpath_deps(pkg):
    """Return immediate or transitive RPATHs depending on the package."""
    if pkg.transitive_rpaths:
        return [d for d in pkg.spec.traverse(root=False, deptype=("link"))]
    else:
        return pkg.spec.dependencies(deptype="link")


def get_rpaths(pkg):
    """Get a list of all the rpaths for a package."""
    rpaths = [pkg.prefix.lib, pkg.prefix.lib64]
    deps = get_rpath_deps(pkg)
    rpaths.extend(d.prefix.lib for d in deps if os.path.isdir(d.prefix.lib))
    rpaths.extend(d.prefix.lib64 for d in deps if os.path.isdir(d.prefix.lib64))
    # Second module is our compiler mod name. We use that to get rpaths from
    # module show output.
    if pkg.compiler.modules and len(pkg.compiler.modules) > 1:
        rpaths.append(path_from_modules([pkg.compiler.modules[1]]))
    return list(dedupe(filter_system_paths(rpaths)))


def load_external_modules(pkg):
    """Traverse a package's spec DAG and load any external modules.

    Traverse a package's dependencies and load any external modules
    associated with them.

    Args:
        pkg (spack.package_base.PackageBase): package to load deps for
    """
    for dep in list(pkg.spec.traverse()):
        external_modules = dep.external_modules or []
        for external_module in external_modules:
            load_module(external_module)


def setup_package(pkg, dirty, context="build"):
    """Execute all environment setup routines."""
    if context not in ["build", "test"]:
        raise ValueError("'context' must be one of ['build', 'test'] - got: {0}".format(context))

    set_module_variables_for_package(pkg)

    # Keep track of env changes from packages separately, since we want to
    # issue warnings when packages make "suspicious" modifications.
    env_base = EnvironmentModifications() if dirty else clean_environment()
    env_mods = EnvironmentModifications()

    # setup compilers for build contexts
    need_compiler = context == "build" or (context == "test" and pkg.test_requires_compiler)
    if need_compiler:
        set_compiler_environment_variables(pkg, env_mods)
        set_wrapper_variables(pkg, env_mods)

    tty.debug("setup_package: grabbing modifications from dependencies")
    env_mods.extend(modifications_from_dependencies(pkg.spec, context, custom_mods_only=False))
    tty.debug("setup_package: collected all modifications from dependencies")

    # architecture specific setup
    platform = spack.platforms.by_name(pkg.spec.architecture.platform)
    target = platform.target(pkg.spec.architecture.target)
    platform.setup_platform_environment(pkg, env_mods)

    if context == "build":
        tty.debug("setup_package: setup build environment for root")
        builder = spack.builder.create(pkg)
        builder.setup_build_environment(env_mods)

        if (not dirty) and (not env_mods.is_unset("CPATH")):
            tty.debug(
                "A dependency has updated CPATH, this may lead pkg-"
                "config to assume that the package is part of the system"
                " includes and omit it when invoked with '--cflags'."
            )
    elif context == "test":
        tty.debug("setup_package: setup test environment for root")
        env_mods.extend(
            inspect_path(
                pkg.spec.prefix,
                spack.user_environment.prefix_inspections(pkg.spec.platform),
                exclude=is_system_path,
            )
        )
        pkg.setup_run_environment(env_mods)
        env_mods.prepend_path("PATH", ".")

    # First apply the clean environment changes
    env_base.apply_modifications()

    # Load modules on an already clean environment, just before applying Spack's
    # own environment modifications. This ensures Spack controls CC/CXX/... variables.
    if need_compiler:
        tty.debug("setup_package: loading compiler modules")
        for mod in pkg.compiler.modules:
            load_module(mod)

    # kludge to handle cray mpich and libsci being automatically loaded by
    # PrgEnv modules on cray platform. Module unload does no damage when
    # unnecessary
    on_cray, _ = _on_cray()
    if on_cray and not dirty:
        for mod in ["cray-mpich", "cray-libsci"]:
            module("unload", mod)

    if target.module_name:
        load_module(target.module_name)

    load_external_modules(pkg)

    implicit_rpaths = pkg.compiler.implicit_rpaths()
    if implicit_rpaths:
        env_mods.set("SPACK_COMPILER_IMPLICIT_RPATHS", ":".join(implicit_rpaths))

    # Make sure nothing's strange about the Spack environment.
    validate(env_mods, tty.warn)
    env_mods.apply_modifications()

    # Return all env modifications we controlled (excluding module related ones)
    env_base.extend(env_mods)
    return env_base


def _make_runnable(pkg, env):
    # Helper method which prepends a Package's bin/ prefix to the PATH
    # environment variable
    prefix = pkg.prefix

    for dirname in ["bin", "bin64"]:
        bin_dir = os.path.join(prefix, dirname)
        if os.path.isdir(bin_dir):
            env.prepend_path("PATH", bin_dir)


def modifications_from_dependencies(
    spec, context, custom_mods_only=True, set_package_py_globals=True
):
    """Returns the environment modifications that are required by
    the dependencies of a spec and also applies modifications
    to this spec's package at module scope, if need be.

    Environment modifications include:

    - Updating PATH so that executables can be found
    - Updating CMAKE_PREFIX_PATH and PKG_CONFIG_PATH so that their respective
      tools can find Spack-built dependencies
    - Running custom package environment modifications

    Custom package modifications can conflict with the default PATH changes
    we make (specifically for the PATH, CMAKE_PREFIX_PATH, and PKG_CONFIG_PATH
    environment variables), so this applies changes in a fixed order:

    - All modifications (custom and default) from external deps first
    - All modifications from non-external deps afterwards

    With that order, `PrependPath` actions from non-external default
    environment modifications will take precedence over custom modifications
    from external packages.

    A secondary constraint is that custom and default modifications are
    grouped on a per-package basis: combined with the post-order traversal this
    means that default modifications of dependents can override custom
    modifications of dependencies (again, this would only occur for PATH,
    CMAKE_PREFIX_PATH, or PKG_CONFIG_PATH).

    Args:
        spec (spack.spec.Spec): spec for which we want the modifications
        context (str): either 'build' for build-time modifications or 'run'
            for run-time modifications
        custom_mods_only (bool): if True returns only custom modifications, if False
            returns custom and default modifications
        set_package_py_globals (bool): whether or not to set the global variables in the
            package.py files (this may be problematic when using buildcaches that have
            been built on a different but compatible OS)
    """
    if context not in ["build", "run", "test"]:
        raise ValueError(
            "Expecting context to be one of ['build', 'run', 'test'], " "got: {0}".format(context)
        )

    env = EnvironmentModifications()

    # Note: see computation of 'custom_mod_deps' and 'exe_deps' later in this
    # function; these sets form the building blocks of those collections.
    build_deps = set(spec.dependencies(deptype=("build", "test")))
    link_deps = set(spec.traverse(root=False, deptype="link"))
    build_link_deps = build_deps | link_deps
    build_and_supporting_deps = set()
    for build_dep in build_deps:
        build_and_supporting_deps.update(build_dep.traverse(deptype="run"))
    run_and_supporting_deps = set(spec.traverse(root=False, deptype=("run", "link")))
    test_and_supporting_deps = set()
    for test_dep in set(spec.dependencies(deptype="test")):
        test_and_supporting_deps.update(test_dep.traverse(deptype="run"))

    # All dependencies that might have environment modifications to apply
    custom_mod_deps = set()
    if context == "build":
        custom_mod_deps.update(build_and_supporting_deps)
        # Tests may be performed after build
        custom_mod_deps.update(test_and_supporting_deps)
    else:
        # test/run context
        custom_mod_deps.update(run_and_supporting_deps)
        if context == "test":
            custom_mod_deps.update(test_and_supporting_deps)
    custom_mod_deps.update(link_deps)

    # Determine 'exe_deps': the set of packages with binaries we want to use
    if context == "build":
        exe_deps = build_and_supporting_deps | test_and_supporting_deps
    elif context == "run":
        exe_deps = set(spec.traverse(deptype="run"))
    elif context == "test":
        exe_deps = test_and_supporting_deps

    def default_modifications_for_dep(dep):
        if dep in build_link_deps and not is_system_path(dep.prefix) and context == "build":
            prefix = dep.prefix

            env.prepend_path("CMAKE_PREFIX_PATH", prefix)

            for directory in ("lib", "lib64", "share"):
                pcdir = os.path.join(prefix, directory, "pkgconfig")
                if os.path.isdir(pcdir):
                    env.prepend_path("PKG_CONFIG_PATH", pcdir)

        if dep in exe_deps and not is_system_path(dep.prefix):
            _make_runnable(dep, env)

    def add_modifications_for_dep(dep):
        tty.debug("Adding env modifications for {0}".format(dep.name))
        # Some callers of this function only want the custom modifications.
        # For callers that want both custom and default modifications, we want
        # to perform the default modifications here (this groups custom
        # and default modifications together on a per-package basis).
        if not custom_mods_only:
            default_modifications_for_dep(dep)

        # Perform custom modifications here (PrependPath actions performed in
        # the custom method override the default environment modifications
        # we do to help the build, namely for PATH, CMAKE_PREFIX_PATH, and
        # PKG_CONFIG_PATH)
        if dep in custom_mod_deps:
            dpkg = dep.package
            if set_package_py_globals:
                set_module_variables_for_package(dpkg)

            current_module = ModuleChangePropagator(spec.package)
            dpkg.setup_dependent_package(current_module, spec)
            current_module.propagate_changes_to_mro()

            if context == "build":
                builder = spack.builder.create(dpkg)
                builder.setup_dependent_build_environment(env, spec)
            else:
                dpkg.setup_dependent_run_environment(env, spec)
        tty.debug("Added env modifications for {0}".format(dep.name))

    # Note that we want to perform environment modifications in a fixed order.
    # The Spec.traverse method provides this: i.e. in addition to
    # the post-order semantics, it also guarantees a fixed traversal order
    # among dependencies which are not constrained by post-order semantics.
    for dspec in spec.traverse(root=False, order="post"):
        if dspec.external:
            add_modifications_for_dep(dspec)

    for dspec in spec.traverse(root=False, order="post"):
        # Default env modifications for non-external packages can override
        # custom modifications of external packages (this can only occur
        # for modifications to PATH, CMAKE_PREFIX_PATH, and PKG_CONFIG_PATH)
        if not dspec.external:
            add_modifications_for_dep(dspec)

    return env


def get_cmake_prefix_path(pkg):
    # Note that unlike modifications_from_dependencies, this does not include
    # any edits to CMAKE_PREFIX_PATH defined in custom
    # setup_dependent_build_environment implementations of dependency packages
    build_deps = set(pkg.spec.dependencies(deptype=("build", "test")))
    link_deps = set(pkg.spec.traverse(root=False, deptype=("link")))
    build_link_deps = build_deps | link_deps
    spack_built = []
    externals = []
    # modifications_from_dependencies updates CMAKE_PREFIX_PATH by first
    # prepending all externals and then all non-externals
    for dspec in pkg.spec.traverse(root=False, order="post"):
        if dspec in build_link_deps:
            if dspec.external:
                externals.insert(0, dspec)
            else:
                spack_built.insert(0, dspec)

    ordered_build_link_deps = spack_built + externals
    cmake_prefix_path_entries = []
    for spec in ordered_build_link_deps:
        cmake_prefix_path_entries.extend(spec.package.cmake_prefix_paths)

    return filter_system_paths(cmake_prefix_path_entries)


def _setup_pkg_and_run(
    serialized_pkg, function, kwargs, write_pipe, input_multiprocess_fd, jsfd1, jsfd2
):
    context = kwargs.get("context", "build")

    try:
        # We are in the child process. Python sets sys.stdin to
        # open(os.devnull) to prevent our process and its parent from
        # simultaneously reading from the original stdin. But, we assume
        # that the parent process is not going to read from it till we
        # are done with the child, so we undo Python's precaution.
        if input_multiprocess_fd is not None:
            sys.stdin = os.fdopen(input_multiprocess_fd.fd)

        pkg = serialized_pkg.restore()

        if not kwargs.get("fake", False):
            kwargs["unmodified_env"] = os.environ.copy()
            kwargs["env_modifications"] = setup_package(
                pkg, dirty=kwargs.get("dirty", False), context=context
            )
        return_value = function(pkg, kwargs)
        write_pipe.send(return_value)

    except StopPhase as e:
        # Do not create a full ChildError from this, it's not an error
        # it's a control statement.
        write_pipe.send(e)
    except BaseException:
        # catch ANYTHING that goes wrong in the child process
        exc_type, exc, tb = sys.exc_info()

        # Need to unwind the traceback in the child because traceback
        # objects can't be sent to the parent.
        tb_string = traceback.format_exc()

        # build up some context from the offending package so we can
        # show that, too.
        package_context = get_package_context(tb)

        logfile = None
        if context == "build":
            try:
                if hasattr(pkg, "log_path"):
                    logfile = pkg.log_path
            except NameError:
                # 'pkg' is not defined yet
                pass
        elif context == "test":
            logfile = os.path.join(pkg.test_suite.stage, pkg.test_suite.test_log_name(pkg.spec))

        error_msg = str(exc)
        if isinstance(exc, (spack.multimethod.NoSuchMethodError, AttributeError)):
            process = "test the installation" if context == "test" else "build from sources"
            error_msg = (
                "The '{}' package cannot find an attribute while trying to {}. "
                "This might be due to a change in Spack's package format "
                "to support multiple build-systems for a single package. You can fix this "
                "by updating the {} recipe, and you can also report the issue as a bug. "
                "More information at https://spack.readthedocs.io/en/latest/packaging_guide.html#installation-procedure"
            ).format(pkg.name, process, context)
            error_msg = colorize("@*R{{{}}}".format(error_msg))
            error_msg = "{}\n\n{}".format(str(exc), error_msg)

        # make a pickleable exception to send to parent.
        msg = "%s: %s" % (exc_type.__name__, error_msg)

        ce = ChildError(
            msg,
            exc_type.__module__,
            exc_type.__name__,
            tb_string,
            logfile,
            context,
            package_context,
        )
        write_pipe.send(ce)

    finally:
        write_pipe.close()
        if input_multiprocess_fd is not None:
            input_multiprocess_fd.close()


def start_build_process(pkg, function, kwargs):
    """Create a child process to do part of a spack build.

    Args:

        pkg (spack.package_base.PackageBase): package whose environment we should set up the
            child process for.
        function (typing.Callable): argless function to run in the child
            process.

    Usage::

        def child_fun():
            # do stuff
        build_env.start_build_process(pkg, child_fun)

    The child process is run with the build environment set up by
    spack.build_environment.  This allows package authors to have full
    control over the environment, etc. without affecting other builds
    that might be executed in the same spack call.

    If something goes wrong, the child process catches the error and
    passes it to the parent wrapped in a ChildError.  The parent is
    expected to handle (or re-raise) the ChildError.

    This uses `multiprocessing.Process` to create the child process. The
    mechanism used to create the process differs on different operating
    systems and for different versions of Python. In some cases "fork"
    is used (i.e. the "fork" system call) and some cases it starts an
    entirely new Python interpreter process (in the docs this is referred
    to as the "spawn" start method). Breaking it down by OS:

    - Linux always uses fork.
    - Mac OS uses fork before Python 3.8 and "spawn" for 3.8 and after.
    - Windows always uses the "spawn" start method.

    For more information on `multiprocessing` child process creation
    mechanisms, see https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
    """
    read_pipe, write_pipe = multiprocessing.Pipe(duplex=False)
    input_multiprocess_fd = None
    jobserver_fd1 = None
    jobserver_fd2 = None

    serialized_pkg = spack.subprocess_context.PackageInstallContext(pkg)

    try:
        # Forward sys.stdin when appropriate, to allow toggling verbosity
        if sys.platform != "win32" and sys.stdin.isatty() and hasattr(sys.stdin, "fileno"):
            input_fd = os.dup(sys.stdin.fileno())
            input_multiprocess_fd = MultiProcessFd(input_fd)
        mflags = os.environ.get("MAKEFLAGS", False)
        if mflags:
            m = re.search(r"--jobserver-[^=]*=(\d),(\d)", mflags)
            if m:
                jobserver_fd1 = MultiProcessFd(int(m.group(1)))
                jobserver_fd2 = MultiProcessFd(int(m.group(2)))

        p = multiprocessing.Process(
            target=_setup_pkg_and_run,
            args=(
                serialized_pkg,
                function,
                kwargs,
                write_pipe,
                input_multiprocess_fd,
                jobserver_fd1,
                jobserver_fd2,
            ),
        )

        p.start()

        # We close the writable end of the pipe now to be sure that p is the
        # only process which owns a handle for it. This ensures that when p
        # closes its handle for the writable end, read_pipe.recv() will
        # promptly report the readable end as being ready.
        write_pipe.close()

    except InstallError as e:
        e.pkg = pkg
        raise

    finally:
        # Close the input stream in the parent process
        if input_multiprocess_fd is not None:
            input_multiprocess_fd.close()

    def exitcode_msg(p):
        typ = "exit" if p.exitcode >= 0 else "signal"
        return f"{typ} {abs(p.exitcode)}"

    try:
        child_result = read_pipe.recv()
    except EOFError:
        p.join()
        raise InstallError(f"The process has stopped unexpectedly ({exitcode_msg(p)})")

    p.join()

    # If returns a StopPhase, raise it
    if isinstance(child_result, StopPhase):
        # do not print
        raise child_result

    # let the caller know which package went wrong.
    if isinstance(child_result, InstallError):
        child_result.pkg = pkg

    if isinstance(child_result, ChildError):
        # If the child process raised an error, print its output here rather
        # than waiting until the call to SpackError.die() in main(). This
        # allows exception handling output to be logged from within Spack.
        # see spack.main.SpackCommand.
        child_result.print_context()
        raise child_result

    # Fallback. Usually caught beforehand in EOFError above.
    if p.exitcode != 0:
        raise InstallError(f"The process failed unexpectedly ({exitcode_msg(p)})")

    return child_result


CONTEXT_BASES = (spack.package_base.PackageBase, spack.build_systems._checks.BaseBuilder)


def get_package_context(traceback, context=3):
    """Return some context for an error message when the build fails.

    Args:
        traceback: A traceback from some exception raised during
            install

        context (int): Lines of context to show before and after the line
            where the error happened

    This function inspects the stack to find where we failed in the
    package file, and it adds detailed context to the long_message
    from there.

    """

    def make_stack(tb, stack=None):
        """Tracebacks come out of the system in caller -> callee order.  Return
        an array in callee -> caller order so we can traverse it."""
        if stack is None:
            stack = []
        if tb is not None:
            make_stack(tb.tb_next, stack)
            stack.append(tb)
        return stack

    stack = make_stack(traceback)

    basenames = tuple(base.__name__ for base in CONTEXT_BASES)
    for tb in stack:
        frame = tb.tb_frame
        if "self" in frame.f_locals:
            # Find the first proper subclass of the PackageBase or BaseBuilder, but
            # don't provide context if the code is actually in the base classes.
            obj = frame.f_locals["self"]
            func = getattr(obj, tb.tb_frame.f_code.co_name, "")
            if func:
                typename, *_ = func.__qualname__.partition(".")
                if isinstance(obj, CONTEXT_BASES) and typename not in basenames:
                    break
    else:
        return None

    # We found obj, the Package implementation we care about.
    # Point out the location in the install method where we failed.
    filename = inspect.getfile(frame.f_code)
    lineno = frame.f_lineno
    if os.path.basename(filename) == "package.py":
        # subtract 1 because we inject a magic import at the top of package files.
        # TODO: get rid of the magic import.
        lineno -= 1

    lines = ["{0}:{1:d}, in {2}:".format(filename, lineno, frame.f_code.co_name)]

    # Build a message showing context in the install method.
    sourcelines, start = inspect.getsourcelines(frame)

    # Calculate lineno of the error relative to the start of the function.
    fun_lineno = lineno - start
    start_ctx = max(0, fun_lineno - context)
    sourcelines = sourcelines[start_ctx : fun_lineno + context + 1]

    for i, line in enumerate(sourcelines):
        is_error = start_ctx + i == fun_lineno
        mark = ">> " if is_error else "   "
        # Add start to get lineno relative to start of file, not function.
        marked = "  {0}{1:-6d}{2}".format(mark, start + start_ctx + i, line.rstrip())
        if is_error:
            marked = colorize("@R{%s}" % cescape(marked))
        lines.append(marked)

    return lines


class ChildError(InstallError):
    """Special exception class for wrapping exceptions from child processes
       in Spack's build environment.

    The main features of a ChildError are:

    1. They're serializable, so when a child build fails, we can send one
       of these to the parent and let the parent report what happened.

    2. They have a ``traceback`` field containing a traceback generated
       on the child immediately after failure.  Spack will print this on
       failure in lieu of trying to run sys.excepthook on the parent
       process, so users will see the correct stack trace from a child.

    3. They also contain context, which shows context in the Package
       implementation where the error happened.  This helps people debug
       Python code in their packages.  To get it, Spack searches the
       stack trace for the deepest frame where ``self`` is in scope and
       is an instance of PackageBase.  This will generally find a useful
       spot in the ``package.py`` file.

    The long_message of a ChildError displays one of two things:

      1. If the original error was a ProcessError, indicating a command
         died during the build, we'll show context from the build log.

      2. If the original error was any other type of error, we'll show
         context from the Python code.

    SpackError handles displaying the special traceback if we're in debug
    mode with spack -d.

    """

    # List of errors considered "build errors", for which we'll show log
    # context instead of Python context.
    build_errors = [("spack.util.executable", "ProcessError")]

    def __init__(self, msg, module, classname, traceback_string, log_name, log_type, context):
        super().__init__(msg)
        self.module = module
        self.name = classname
        self.traceback = traceback_string
        self.log_name = log_name
        self.log_type = log_type
        self.context = context

    @property
    def long_message(self):
        out = io.StringIO()
        out.write(self._long_message if self._long_message else "")

        have_log = self.log_name and os.path.exists(self.log_name)

        if (self.module, self.name) in ChildError.build_errors:
            # The error happened in some external executed process. Show
            # the log with errors or warnings highlighted.
            if have_log:
                write_log_summary(out, self.log_type, self.log_name)

        else:
            # The error happened in the Python code, so try to show
            # some context from the Package itself.
            if self.context:
                out.write("\n")
                out.write("\n".join(self.context))
                out.write("\n")

        if out.getvalue():
            out.write("\n")

        if have_log:
            out.write("See {0} log for details:\n".format(self.log_type))
            out.write("  {0}\n".format(self.log_name))

        # Also output the test log path IF it exists
        if self.context != "test":
            test_log = join_path(os.path.dirname(self.log_name), spack_install_test_log)
            if os.path.isfile(test_log):
                out.write("\nSee test log for details:\n")
                out.write("  {0}\n".format(test_log))

        return out.getvalue()

    def __str__(self):
        return self.message

    def __reduce__(self):
        """__reduce__ is used to serialize (pickle) ChildErrors.

        Return a function to reconstruct a ChildError, along with the
        salient properties we'll need.
        """
        return _make_child_error, (
            self.message,
            self.module,
            self.name,
            self.traceback,
            self.log_name,
            self.log_type,
            self.context,
        )


def _make_child_error(msg, module, name, traceback, log, log_type, context):
    """Used by __reduce__ in ChildError to reconstruct pickled errors."""
    return ChildError(msg, module, name, traceback, log, log_type, context)


class StopPhase(spack.error.SpackError):
    """Pickle-able exception to control stopped builds."""

    def __reduce__(self):
        return _make_stop_phase, (self.message, self.long_message)


def _make_stop_phase(msg, long_msg):
    return StopPhase(msg, long_msg)


def write_log_summary(out, log_type, log, last=None):
    errors, warnings = parse_log_events(log)
    nerr = len(errors)
    nwar = len(warnings)

    if nerr > 0:
        if last and nerr > last:
            errors = errors[-last:]
            nerr = last

        # If errors are found, only display errors
        out.write("\n%s found in %s log:\n" % (plural(nerr, "error"), log_type))
        out.write(make_log_context(errors))
    elif nwar > 0:
        if last and nwar > last:
            warnings = warnings[-last:]
            nwar = last

        # If no errors are found but warnings are, display warnings
        out.write("\n%s found in %s log:\n" % (plural(nwar, "warning"), log_type))
        out.write(make_log_context(warnings))


class ModuleChangePropagator:
    """Wrapper class to accept changes to a package.py Python module, and propagate them in the
    MRO of the package.

    It is mainly used as a substitute of the ``package.py`` module, when calling the
    "setup_dependent_package" function during build environment setup.
    """

    _PROTECTED_NAMES = ("package", "current_module", "modules_in_mro", "_set_attributes")

    def __init__(self, package):
        self._set_self_attributes("package", package)
        self._set_self_attributes("current_module", package.module)

        #: Modules for the classes in the MRO up to PackageBase
        modules_in_mro = []
        for cls in inspect.getmro(type(package)):
            module = cls.module

            if module == self.current_module:
                continue

            if module == spack.package_base:
                break

            modules_in_mro.append(module)
        self._set_self_attributes("modules_in_mro", modules_in_mro)
        self._set_self_attributes("_set_attributes", {})

    def _set_self_attributes(self, key, value):
        super().__setattr__(key, value)

    def __getattr__(self, item):
        return getattr(self.current_module, item)

    def __setattr__(self, key, value):
        if key in ModuleChangePropagator._PROTECTED_NAMES:
            msg = f'Cannot set attribute "{key}" in ModuleMonkeyPatcher'
            return AttributeError(msg)

        setattr(self.current_module, key, value)
        self._set_attributes[key] = value

    def propagate_changes_to_mro(self):
        for module_in_mro in self.modules_in_mro:
            module_in_mro.__dict__.update(self._set_attributes)
