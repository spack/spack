# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""spack.package defines the public API for Spack packages, by re-exporting useful symbols from
other modules. Packages should import this module, instead of importing from spack.* directly
to ensure forward compatibility with future versions of Spack."""

import warnings
from os import chdir, environ, getcwd, makedirs, mkdir, remove, removedirs
from shutil import move, rmtree

# import most common types used in packages
from typing import Dict, Iterable, List, Optional

from spack.vendor.macholib.MachO import LC_ID_DYLIB, MachO

import spack.builder
from spack.archspec import microarchitecture_flags, microarchitecture_flags_from_target
from spack.build_environment import (
    MakeExecutable,
    ModuleChangePropagator,
    get_cmake_prefix_path,
    get_effective_jobs,
    shared_library_suffix,
    static_library_suffix,
)
from spack.builder import (
    BaseBuilder,
    Builder,
    BuilderWithDefaults,
    GenericBuilder,
    Package,
    apply_macos_rpath_fixups,
    execute_install_time_tests,
    register_builder,
)
from spack.compilers.config import find_compilers
from spack.compilers.libraries import CompilerPropertyDetector, compiler_spec
from spack.config import determine_number_of_jobs
from spack.deptypes import ALL_TYPES as all_deptypes
from spack.directives import (
    build_system,
    can_splice,
    conditional,
    conflicts,
    depends_on,
    extends,
    license,
    maintainers,
    patch,
    provides,
    redistribute,
    requires,
    resource,
    variant,
    version,
)
from spack.error import (
    CompilerError,
    InstallError,
    NoHeadersError,
    NoLibrariesError,
    SpackAPIWarning,
    SpackError,
)
from spack.hooks.sbang import filter_shebang, sbang_install_path, sbang_shebang_line
from spack.install_test import (
    SkipTest,
    cache_extra_test_sources,
    check_outputs,
    find_required_file,
    get_escaped_text_output,
    install_test_root,
    test_part,
)
from spack.llnl.util.filesystem import (
    FileFilter,
    FileList,
    HeaderList,
    LibraryList,
    ancestor,
    can_access,
    change_sed_delimiter,
    copy,
    copy_tree,
    filter_file,
    find,
    find_all_headers,
    find_all_libraries,
    find_first,
    find_headers,
    find_libraries,
    find_system_libraries,
    force_remove,
    force_symlink,
    has_shebang,
    install,
    install_tree,
    is_exe,
    join_path,
    keep_modification_time,
    library_extensions,
    make_package_test_rpath,
    mkdirp,
    path_contains_subdirectory,
    readlink,
    remove_directory_contents,
    remove_linked_tree,
    rename,
    safe_remove,
    set_executable,
    set_install_permissions,
    symlink,
    touch,
    windows_sfn,
    working_dir,
)
from spack.llnl.util.lang import ClassProperty, classproperty, dedupe, memoized
from spack.llnl.util.link_tree import LinkTree
from spack.mixins import filter_compiler_wrappers
from spack.multimethod import default_args, when
from spack.operating_systems.linux_distro import kernel_version
from spack.operating_systems.mac_os import macos_version
from spack.package_base import (
    PackageBase,
    build_system_flags,
    env_flags,
    inject_flags,
    on_package_attributes,
)
from spack.package_completions import (
    bash_completion_path,
    fish_completion_path,
    zsh_completion_path,
)
from spack.package_test import compare_output, compare_output_file, compile_c_and_execute
from spack.paths import spack_script
from spack.phase_callbacks import run_after, run_before
from spack.platforms import host as host_platform
from spack.spec import Spec
from spack.url import substitute_version as substitute_version_in_url
from spack.user_environment import environment_modifications_for_specs
from spack.util.elf import delete_needed_from_elf, delete_rpath, get_elf_compat, parse_elf
from spack.util.environment import EnvironmentModifications
from spack.util.environment import filter_system_paths as _filter_system_paths
from spack.util.environment import is_system_path as _is_system_path
from spack.util.environment import set_env
from spack.util.executable import Executable, ProcessError, which, which_string
from spack.util.filesystem import fix_darwin_install_name
from spack.util.libc import libc_from_dynamic_linker, parse_dynamic_linker
from spack.util.module_cmd import get_path_args_from_module_line
from spack.util.module_cmd import module as module_command
from spack.util.path import get_user
from spack.util.prefix import Prefix
from spack.util.url import join as join_url
from spack.util.windows_registry import HKEY, WindowsRegistryView
from spack.variant import any_combination_of, auto_or_any_combination_of, disjoint_sets
from spack.version import Version, ver

#: alias for ``os.environ``
env = environ

#: alias for ``os.chdir``
cd = chdir

#: alias for ``os.getcwd``
pwd = getcwd

# Not an import alias because black and isort disagree about style
create_builder = spack.builder.create


class tty:
    import spack.llnl.util.tty as _tty

    debug = _tty.debug
    error = _tty.error
    info = _tty.info
    msg = _tty.msg
    warn = _tty.warn


def is_system_path(path: str) -> bool:
    """Returns True if the argument is a system path, False otherwise."""
    warnings.warn(
        "spack.package.is_system_path is deprecated", category=SpackAPIWarning, stacklevel=2
    )
    return _is_system_path(path)


def filter_system_paths(paths: Iterable[str]) -> List[str]:
    """Returns a copy of the input where system paths are filtered out."""
    warnings.warn(
        "spack.package.filter_system_paths is deprecated", category=SpackAPIWarning, stacklevel=2
    )
    return _filter_system_paths(paths)


__all__ = [
    # v2.0
    "BaseBuilder",
    "Builder",
    "Dict",
    "EnvironmentModifications",
    "Executable",
    "FileFilter",
    "FileList",
    "HeaderList",
    "InstallError",
    "LibraryList",
    "List",
    "MakeExecutable",
    "NoHeadersError",
    "NoLibrariesError",
    "Optional",
    "PackageBase",
    "Prefix",
    "ProcessError",
    "SkipTest",
    "Spec",
    "Version",
    "all_deptypes",
    "ancestor",
    "any_combination_of",
    "auto_or_any_combination_of",
    "bash_completion_path",
    "build_system_flags",
    "build_system",
    "cache_extra_test_sources",
    "can_access",
    "can_splice",
    "cd",
    "change_sed_delimiter",
    "check_outputs",
    "conditional",
    "conflicts",
    "copy_tree",
    "copy",
    "default_args",
    "depends_on",
    "determine_number_of_jobs",
    "disjoint_sets",
    "env_flags",
    "env",
    "extends",
    "filter_compiler_wrappers",
    "filter_file",
    "find_all_headers",
    "find_first",
    "find_headers",
    "find_libraries",
    "find_required_file",
    "find_system_libraries",
    "find",
    "fish_completion_path",
    "fix_darwin_install_name",
    "force_remove",
    "force_symlink",
    "get_escaped_text_output",
    "inject_flags",
    "install_test_root",
    "install_tree",
    "install",
    "is_exe",
    "join_path",
    "keep_modification_time",
    "library_extensions",
    "license",
    "maintainers",
    "makedirs",
    "mkdir",
    "mkdirp",
    "move",
    "on_package_attributes",
    "patch",
    "provides",
    "pwd",
    "redistribute",
    "register_builder",
    "remove_directory_contents",
    "remove_linked_tree",
    "remove",
    "removedirs",
    "rename",
    "requires",
    "resource",
    "rmtree",
    "run_after",
    "run_before",
    "set_executable",
    "set_install_permissions",
    "symlink",
    "test_part",
    "touch",
    "tty",
    "variant",
    "ver",
    "version",
    "when",
    "which_string",
    "which",
    "working_dir",
    "zsh_completion_path",
    # v2.1
    "CompilerError",
    "SpackError",
    # v2.2
    "BuilderWithDefaults",
    "ClassProperty",
    "CompilerPropertyDetector",
    "GenericBuilder",
    "HKEY",
    "LC_ID_DYLIB",
    "LinkTree",
    "MachO",
    "ModuleChangePropagator",
    "Package",
    "WindowsRegistryView",
    "apply_macos_rpath_fixups",
    "classproperty",
    "compare_output_file",
    "compare_output",
    "compile_c_and_execute",
    "compiler_spec",
    "create_builder",
    "dedupe",
    "delete_needed_from_elf",
    "delete_rpath",
    "environment_modifications_for_specs",
    "execute_install_time_tests",
    "filter_shebang",
    "filter_system_paths",
    "find_all_libraries",
    "find_compilers",
    "get_cmake_prefix_path",
    "get_effective_jobs",
    "get_elf_compat",
    "get_path_args_from_module_line",
    "get_user",
    "has_shebang",
    "host_platform",
    "is_system_path",
    "join_url",
    "kernel_version",
    "libc_from_dynamic_linker",
    "macos_version",
    "make_package_test_rpath",
    "memoized",
    "microarchitecture_flags_from_target",
    "microarchitecture_flags",
    "module_command",
    "parse_dynamic_linker",
    "parse_elf",
    "path_contains_subdirectory",
    "readlink",
    "safe_remove",
    "sbang_install_path",
    "sbang_shebang_line",
    "set_env",
    "shared_library_suffix",
    "spack_script",
    "static_library_suffix",
    "substitute_version_in_url",
    "windows_sfn",
]

# These are just here for editor support; they may be set when the build env is set up.
configure: Executable
make_jobs: int
make: MakeExecutable
nmake: Executable
ninja: MakeExecutable
python_include: str
python_platlib: str
python_purelib: str
python: Executable
spack_cc: str
spack_cxx: str
spack_f77: str
spack_fc: str
prefix: Prefix
dso_suffix: str
