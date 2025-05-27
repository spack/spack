# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""spack.package defines the public API for Spack packages, by re-exporting useful symbols from
other modules. Packages should import this module, instead of importing from spack.* directly
to ensure forward compatibility with future versions of Spack."""

from os import chdir, environ, getcwd, makedirs, mkdir, remove, removedirs
from shutil import move, rmtree

# import most common types used in packages
from typing import Dict, List, Optional

from llnl.util.filesystem import (
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
    find_first,
    find_headers,
    find_libraries,
    find_system_libraries,
    force_remove,
    force_symlink,
    install,
    install_tree,
    is_exe,
    join_path,
    keep_modification_time,
    library_extensions,
    mkdirp,
    remove_directory_contents,
    remove_linked_tree,
    rename,
    set_executable,
    set_install_permissions,
    touch,
    working_dir,
)
from llnl.util.symlink import symlink

from spack.build_environment import MakeExecutable
from spack.builder import BaseBuilder, Builder, register_builder
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
from spack.error import InstallError, NoHeadersError, NoLibrariesError
from spack.install_test import (
    SkipTest,
    cache_extra_test_sources,
    check_outputs,
    find_required_file,
    get_escaped_text_output,
    install_test_root,
    test_part,
)
from spack.mixins import filter_compiler_wrappers
from spack.multimethod import default_args, when
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
from spack.phase_callbacks import run_after, run_before
from spack.spec import Spec
from spack.util.environment import EnvironmentModifications
from spack.util.executable import Executable, ProcessError, which, which_string
from spack.util.filesystem import fix_darwin_install_name
from spack.util.prefix import Prefix
from spack.variant import any_combination_of, auto_or_any_combination_of, disjoint_sets
from spack.version import Version, ver

# Emulate some shell commands for convenience
env = environ
cd = chdir
pwd = getcwd


class tty:
    import llnl.util.tty as _tty

    debug = _tty.debug
    error = _tty.error
    info = _tty.info
    msg = _tty.msg
    warn = _tty.warn


__all__ = [
    "chdir",
    "environ",
    "getcwd",
    "makedirs",
    "mkdir",
    "remove",
    "removedirs",
    "move",
    "rmtree",
    "Dict",
    "List",
    "Optional",
    "FileFilter",
    "FileList",
    "HeaderList",
    "LibraryList",
    "ancestor",
    "can_access",
    "change_sed_delimiter",
    "copy",
    "copy_tree",
    "filter_file",
    "find",
    "find_all_headers",
    "find_first",
    "find_headers",
    "find_libraries",
    "find_system_libraries",
    "force_remove",
    "force_symlink",
    "install",
    "install_tree",
    "is_exe",
    "join_path",
    "keep_modification_time",
    "library_extensions",
    "mkdirp",
    "remove_directory_contents",
    "remove_linked_tree",
    "rename",
    "set_executable",
    "set_install_permissions",
    "touch",
    "working_dir",
    "symlink",
    "MakeExecutable",
    "BaseBuilder",
    "determine_number_of_jobs",
    "all_deptypes",
    "build_system",
    "can_splice",
    "conditional",
    "conflicts",
    "depends_on",
    "extends",
    "license",
    "maintainers",
    "patch",
    "provides",
    "redistribute",
    "requires",
    "resource",
    "variant",
    "version",
    "InstallError",
    "NoHeadersError",
    "NoLibrariesError",
    "SkipTest",
    "cache_extra_test_sources",
    "check_outputs",
    "find_required_file",
    "get_escaped_text_output",
    "install_test_root",
    "test_part",
    "filter_compiler_wrappers",
    "default_args",
    "when",
    "build_system_flags",
    "env_flags",
    "inject_flags",
    "on_package_attributes",
    "bash_completion_path",
    "fish_completion_path",
    "zsh_completion_path",
    "run_after",
    "run_before",
    "Spec",
    "EnvironmentModifications",
    "Executable",
    "ProcessError",
    "which",
    "which_string",
    "fix_darwin_install_name",
    "Prefix",
    "any_combination_of",
    "auto_or_any_combination_of",
    "disjoint_sets",
    "Version",
    "ver",
    "env",
    "cd",
    "pwd",
    "tty",
    "Builder",
    "PackageBase",
    "register_builder",
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
