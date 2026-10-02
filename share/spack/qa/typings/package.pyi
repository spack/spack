from _typeshed import Incomplete
from os import chdir, environ, getcwd, makedirs as makedirs, mkdir as mkdir, remove as remove, removedirs as removedirs
from shutil import move as move, rmtree as rmtree
from spack.archspec import microarchitecture_flags as microarchitecture_flags, microarchitecture_flags_from_target as microarchitecture_flags_from_target
from spack.build_environment import MakeExecutable as MakeExecutable, ModuleChangePropagator as ModuleChangePropagator, get_cmake_prefix_path as get_cmake_prefix_path, get_effective_jobs as get_effective_jobs, shared_library_suffix as shared_library_suffix, static_library_suffix as static_library_suffix
from spack.builder import BaseBuilder as BaseBuilder, Builder as Builder, BuilderWithDefaults as BuilderWithDefaults, GenericBuilder as GenericBuilder, Package as Package, apply_macos_rpath_fixups as apply_macos_rpath_fixups, execute_install_time_tests as execute_install_time_tests, register_builder as register_builder
from spack.compilers.config import find_compilers as find_compilers
from spack.compilers.libraries import CompilerPropertyDetector as CompilerPropertyDetector, compiler_spec as compiler_spec
from spack.config import determine_number_of_jobs as determine_number_of_jobs
from spack.deptypes import ALL_TYPES as all_deptypes
from spack.directives import build_system as build_system, can_splice as can_splice, conditional as conditional, conflicts as conflicts, depends_on as depends_on, extends as extends, license as license, maintainers as maintainers, patch as patch, provides as provides, redistribute as redistribute, requires as requires, resource as resource, variant as variant, version as version
from spack.error import CompilerError as CompilerError, InstallError as InstallError, NoHeadersError as NoHeadersError, NoLibrariesError as NoLibrariesError, SpackError as SpackError
from spack.hooks.sbang import filter_shebang as filter_shebang, sbang_install_path as sbang_install_path, sbang_shebang_line as sbang_shebang_line
from spack.install_test import SkipTest as SkipTest, cache_extra_test_sources as cache_extra_test_sources, check_outputs as check_outputs, find_required_file as find_required_file, get_escaped_text_output as get_escaped_text_output, install_test_root as install_test_root, test_part as test_part
from spack.llnl.util.filesystem import FileFilter as FileFilter, FileList as FileList, HeaderList as HeaderList, LibraryList as LibraryList, ancestor as ancestor, can_access as can_access, change_sed_delimiter as change_sed_delimiter, copy as copy, copy_tree as copy_tree, filter_file as filter_file, find as find, find_all_headers as find_all_headers, find_all_libraries as find_all_libraries, find_first as find_first, find_headers as find_headers, find_libraries as find_libraries, find_system_libraries as find_system_libraries, force_remove as force_remove, force_symlink as force_symlink, has_shebang as has_shebang, install as install, install_tree as install_tree, is_exe as is_exe, join_path as join_path, keep_modification_time as keep_modification_time, library_extensions as library_extensions, mkdirp as mkdirp, path_contains_subdirectory as path_contains_subdirectory, readlink as readlink, remove_directory_contents as remove_directory_contents, remove_linked_tree as remove_linked_tree, rename as rename, safe_remove as safe_remove, set_executable as set_executable, set_install_permissions as set_install_permissions, symlink as symlink, touch as touch, windows_sfn as windows_sfn, working_dir as working_dir
from spack.llnl.util.lang import ClassProperty as ClassProperty, classproperty as classproperty, dedupe as dedupe, memoized as memoized
from spack.llnl.util.link_tree import LinkTree as LinkTree
from spack.mixins import filter_compiler_wrappers as filter_compiler_wrappers
from spack.multimethod import default_args as default_args, when as when
from spack.operating_systems.linux_distro import kernel_version as kernel_version
from spack.operating_systems.mac_os import macos_version as macos_version
from spack.package_base import PackageBase as PackageBase, make_package_test_rpath as make_package_test_rpath, on_package_attributes as on_package_attributes
from spack.package_completions import bash_completion_path as bash_completion_path, fish_completion_path as fish_completion_path, zsh_completion_path as zsh_completion_path
from spack.package_test import compare_output as compare_output, compare_output_file as compare_output_file, compile_c_and_execute as compile_c_and_execute
from spack.paths import spack_script as spack_script
from spack.phase_callbacks import run_after as run_after, run_before as run_before
from spack.platforms import host as host_platform
from spack.spec import Spec as Spec
from spack.url import substitute_version as substitute_version_in_url
from spack.user_environment import environment_modifications_for_specs as environment_modifications_for_specs
from spack.util.elf import delete_needed_from_elf as delete_needed_from_elf, delete_rpath as delete_rpath, get_elf_compat as get_elf_compat, parse_elf as parse_elf
from spack.util.environment import EnvironmentModifications as EnvironmentModifications, set_env as set_env
from spack.util.executable import Executable as Executable, ProcessError as ProcessError, which as which, which_string as which_string
from spack.util.filesystem import fix_darwin_install_name as fix_darwin_install_name
from spack.util.libc import libc_from_dynamic_linker as libc_from_dynamic_linker, parse_dynamic_linker as parse_dynamic_linker
from spack.util.module_cmd import get_path_args_from_module_line as get_path_args_from_module_line, module as module_command
from spack.util.path import get_user as get_user
from spack.util.prefix import Prefix as Prefix
from spack.util.url import join as join_url
from spack.util.windows_registry import HKEY as HKEY, WindowsRegistryView as WindowsRegistryView
from spack.variant import any_combination_of as any_combination_of, auto_or_any_combination_of as auto_or_any_combination_of, disjoint_sets as disjoint_sets
from spack.vendor.macholib.MachO import LC_ID_DYLIB as LC_ID_DYLIB, MachO as MachO
from spack.version import Version as Version, ver as ver
from typing import Dict as Dict, Iterable, List as List, Optional as Optional

__all__ = ['BaseBuilder', 'Builder', 'Dict', 'EnvironmentModifications', 'Executable', 'FileFilter', 'FileList', 'HeaderList', 'InstallError', 'LibraryList', 'List', 'MakeExecutable', 'NoHeadersError', 'NoLibrariesError', 'Optional', 'PackageBase', 'Prefix', 'ProcessError', 'SkipTest', 'Spec', 'Version', 'all_deptypes', 'ancestor', 'any_combination_of', 'auto_or_any_combination_of', 'bash_completion_path', 'build_system_flags', 'build_system', 'cache_extra_test_sources', 'can_access', 'can_splice', 'cd', 'change_sed_delimiter', 'check_outputs', 'conditional', 'conflicts', 'copy_tree', 'copy', 'default_args', 'depends_on', 'determine_number_of_jobs', 'disjoint_sets', 'env_flags', 'env', 'extends', 'filter_compiler_wrappers', 'filter_file', 'find_all_headers', 'find_first', 'find_headers', 'find_libraries', 'find_required_file', 'find_system_libraries', 'find', 'fish_completion_path', 'fix_darwin_install_name', 'force_remove', 'force_symlink', 'get_escaped_text_output', 'inject_flags', 'install_test_root', 'install_tree', 'install', 'is_exe', 'join_path', 'keep_modification_time', 'library_extensions', 'license', 'maintainers', 'makedirs', 'mkdir', 'mkdirp', 'move', 'on_package_attributes', 'patch', 'provides', 'pwd', 'redistribute', 'register_builder', 'remove_directory_contents', 'remove_linked_tree', 'remove', 'removedirs', 'rename', 'requires', 'resource', 'rmtree', 'run_after', 'run_before', 'set_executable', 'set_install_permissions', 'symlink', 'test_part', 'touch', 'tty', 'variant', 'ver', 'version', 'when', 'which_string', 'which', 'working_dir', 'zsh_completion_path', 'CompilerError', 'SpackError', 'BuilderWithDefaults', 'ClassProperty', 'CompilerPropertyDetector', 'GenericBuilder', 'HKEY', 'LC_ID_DYLIB', 'LinkTree', 'MachO', 'ModuleChangePropagator', 'Package', 'WindowsRegistryView', 'apply_macos_rpath_fixups', 'classproperty', 'compare_output_file', 'compare_output', 'compile_c_and_execute', 'compiler_spec', 'create_builder', 'dedupe', 'delete_needed_from_elf', 'delete_rpath', 'environment_modifications_for_specs', 'execute_install_time_tests', 'filter_shebang', 'filter_system_paths', 'find_all_libraries', 'find_compilers', 'get_cmake_prefix_path', 'get_effective_jobs', 'get_elf_compat', 'get_path_args_from_module_line', 'get_user', 'has_shebang', 'host_platform', 'is_system_path', 'join_url', 'kernel_version', 'libc_from_dynamic_linker', 'macos_version', 'make_package_test_rpath', 'memoized', 'microarchitecture_flags_from_target', 'microarchitecture_flags', 'module_command', 'parse_dynamic_linker', 'parse_elf', 'path_contains_subdirectory', 'readlink', 'safe_remove', 'sbang_install_path', 'sbang_shebang_line', 'set_env', 'shared_library_suffix', 'spack_script', 'static_library_suffix', 'substitute_version_in_url', 'windows_sfn']

env = environ
cd = chdir
pwd = getcwd
rename = rename
makedirs = makedirs
mkdir = mkdir
remove = remove
removedirs = removedirs
move = move
rmtree = rmtree
readlink = readlink
rename = rename
symlink = symlink
create_builder: Incomplete
MachO = MachO
LC_ID_DYLIB = LC_ID_DYLIB

class tty:
    debug: Incomplete
    error: Incomplete
    info: Incomplete
    msg: Incomplete
    warn: Incomplete

def is_system_path(path: str) -> bool: ...
def filter_system_paths(paths: Iterable[str]) -> list[str]: ...

build_system_flags: Incomplete
env_flags: Incomplete
inject_flags: Incomplete
