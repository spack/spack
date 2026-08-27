# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import ctypes
import itertools
import os
import re
import struct
import sys
from typing import IO, Dict, Iterable, List, Optional

import spack.vendor.macholib.mach_o
import spack.vendor.macholib.MachO

import spack.error
import spack.spec
import spack.store
import spack.util.elf as elf
import spack.util.executable as executable
import spack.util.filesystem as fs
import spack.util.lang
from spack.util import elf, executable, tty
from spack.util.environment import EnvironmentModifications
from spack.util.filesystem import readlink, symlink
from spack.util.lang import memoized

from .relocate_text import BinaryFilePrefixReplacer, PrefixToPrefix, TextFilePrefixReplacer

if sys.platform == "win32":
    import ctypes.wintypes


WRAPPER_NAME_LEN = 143


@memoized
def _patchelf() -> Optional[executable.Executable]:
    """Return the full path to the patchelf binary, if available, else None."""
    import spack.bootstrap

    if sys.platform == "darwin":
        return None

    with spack.bootstrap.ensure_bootstrap_configuration():
        return spack.bootstrap.ensure_patchelf_in_path_or_raise()


def _decode_macho_data(bytestring):
    return bytestring.rstrip(b"\x00").decode("ascii")


def setup_relocate_run(wrapper_spec) -> executable.Executable:
    """Establishes environment neccesary to run the relocate utility, returns the
    executable with the properly established environment."""
    import spack.user_environment

    relocate_exe = executable.Executable(str(wrapper_spec.package.bin_dir() / "relocate.exe"))  # type: ignore
    # get msvc context from wrapper - needed for finding msvc utils during relocate run
    relocate_exe.add_default_envmod(
        spack.user_environment.environment_modifications_for_specs(
            wrapper_spec, set_package_py_globals=False
        )
    )
    return relocate_exe


def bootstrap_relocate() -> executable.Executable:
    """Bootstraps and returns an executable reference to the Windows compiler
    wrappers relocate utility"""
    import spack.bootstrap as bootstrapper

    with bootstrapper.ensure_bootstrap_configuration():
        # ensure_msvc_relocate_or_raise() may hand back a bare relocate.exe found
        # via a PATH search, with no MSVC environment attached (see the early
        # return in ensure_executables_in_path_or_raise). relocate.exe needs the
        # vcvars-derived INCLUDE/LIB/PATH to find msvc utils (link.exe, lib.exe,
        # dumpbin.exe, ...), so don't trust its return value: look up the
        # concrete compiler-wrapper spec ourselves and always attach its
        # environment, the same way setup_relocate_run does.
        bootstrapper.ensure_msvc_relocate_or_raise()
        wrapper_spec = next(
            iter(spack.store.STORE.db.query_local("compiler-wrapper", installed=True)), None
        )
        if not wrapper_spec:
            raise RuntimeError(
                "Failed to bootstrap the MSVC compiler wrapper: no compiler-wrapper spec "
                "found in the bootstrap store after bootstrapping relocate.exe"
            )
        return setup_relocate_run(wrapper_spec)


def relocate(spec=None) -> executable.Executable:
    """Relocate binaries for 'spec' on Windows."""
    wrapper_spec = None
    if spec:
        try:
            wrapper_spec = spec["compiler-wrapper"]
        except KeyError:
            pass
    if not wrapper_spec:
        # We need to bootstrap
        return bootstrap_relocate()
    return setup_relocate_run(wrapper_spec)


def apply_pe_relocations(
    pe_targets: Iterable[str],
    coff_for_target: Dict[str, str],
    reloc_exe: executable.Executable,
    ev: EnvironmentModifications,
    **reloc_kwargs,
) -> None:
    """Invoke the compiler wrapper's relocate executable on each PE target (dll or
    exe). PE files may or may not export symbols (most exes and plugin dlls do not),
    but references to other PE files inside them still need relocating either way.
    If ``coff_for_target`` has an import library recorded for a given target, it's
    passed along via ``--coff`` so the wrapper regenerates its exports to point at
    the relocated import library.
    """
    for pe in pe_targets:
        args = ["--pe", pe]
        args.append("--full")
        if pe in coff_for_target:
            args.extend(["--coff", coff_for_target[pe]])
        reloc_exe(*args, extra_env=ev, **reloc_kwargs)


def _prefix_matcher(prefixes: Dict[str, str]):
    """Build a (regex, lookup) pair for matching Windows path prefixes.

    Windows paths are case insensitive, and the compiler wrapper hands back paths in
    whatever casing the linker recorded - 8.3 short names in particular always come
    back from ``GetShortPathNameW`` in upper case. So the match has to be case
    insensitive, and because ``match.group()`` returns text in the *subject's* casing
    rather than the dict key's, the resulting prefix has to be looked up through a
    case folded map.

    Prefixes are sorted longest first so that ``C:\\opt\\pkg`` wins over ``C:\\opt``,
    matching the behavior of :func:`_macho_find_paths`.
    """
    ordered = sorted(prefixes, key=len, reverse=True)
    regex = re.compile("|".join(re.escape(p) for p in ordered), re.IGNORECASE)
    lookup = {p.lower(): prefixes[p] for p in ordered}
    return regex, lookup


def _import_lib_targets(
    targets: List[str],
    all_prefixes: Dict[str, str],
    reloc_exe: Optional[executable.Executable] = None,
    stage: Optional[bool] = False,
) -> Dict[str, str]:
    """Match each import library's referenced DLL against ``all_prefixes`` (old
    prefix -> new prefix, including any SFN forms) for the buildcache
    or a straightforward stage -> install prefix mapping for the stage.
    Returns a mapping from the DLL's new absolute path to the import library's
    new absolute path, for use as the ``--coff`` argument when relocating that DLL/exe.
    """
    if not all_prefixes:
        # An empty alternation compiles to a regex that matches everything with an
        # empty match, which would map every DLL onto the "" prefix.
        tty.debug("No prefixes to relocate, skipping import library association...")
        return {}
    libs = [t for t in targets if t.lower().endswith(".lib")]
    regex, prefix_lookup = _prefix_matcher(all_prefixes)
    coff_for_target: Dict[str, str] = {}
    for lib in libs:
        # we relocate exes and dlls, import libraries are regenerated
        # with a new dll pointer from the existing import library
        # static .libs are ignored (.lib is any coff library on Windows,
        # which covers both import and static libraries)
        # Dlls have no references to their import libraries
        # but import libraries reference dlls, so although
        # the DLLs are our "relocation targets" we drive that
        # via import libs to determine the proper association
        if verify_import_lib(lib, reloc_exe=reloc_exe):
            dll_path = get_importlib_target(lib, reloc_exe=reloc_exe)
            if not dll_path:
                tty.debug(
                    f"Import lib {lib} does not reference a compatible DLL, skipping relocation..."
                )
                continue
            # The wrapper pads the DLL path it stores in the import library out to a
            # fixed width with path separators; normpath collapses that padding back
            # into the real path.
            norm_dll_path = os.path.normpath(dll_path)
            # matches prefix component in dll_path inside import library
            # which is the absolute path to the dll the import library corresponds to
            # on the machine/stage where this import library was built
            match = regex.match(norm_dll_path)
            if match:
                old_root = match.group()
                new_root = prefix_lookup[old_root.lower()]
                if stage:
                    new_dll_path = new_root
                else:
                    dll_name = os.path.relpath(norm_dll_path, old_root)
                    new_dll_path = os.path.join(new_root, dll_name)
                coff_for_target[new_dll_path] = lib
            else:
                tty.warn(
                    f"Import lib: {lib} does not reference a DLL "
                    "in this prefix, skipping relocation...\n"
                    f"Prefixes failed to map: {all_prefixes}"
                )
    return coff_for_target


def _check_wrapper_can_record(pe_targets: List[str], spec: spack.spec.Spec) -> None:
    """Fail loudly when the wrapper has no way to store a PE's path.

    Relocation works by rewriting the absolute paths the wrapper baked into each PE, so
    a path it could not record in the first place leaves that binary pointing somewhere
    wrong. That surfaces as a load failure long after the install, so catch it here
    instead of shipping binaries with unresolvable DLL references.
    """
    too_long = [pe for pe in pe_targets if len(pe) > WRAPPER_NAME_LEN]
    if not too_long:
        return
    # Only probe the filesystem once we know something actually needs the fallback.
    if fs.short_filenames_enabled(str(spec.prefix)):
        return
    listed = "\n  ".join(too_long[:5])
    remaining = len(too_long) - 5
    if remaining > 0:
        listed += f"\n  ... and {remaining} more"
    raise WindowsPathTooLongError(
        f"Cannot relocate {spec.name}: {len(too_long)} binaries have paths longer than "
        f"the {WRAPPER_NAME_LEN} characters the compiler wrapper can record, and 8.3 "
        f"short filenames are not enabled on this volume.",
        f"Affected binaries:\n  {listed}\n\n"
        f"The install prefix is {len(str(spec.prefix))} characters:\n"
        f"  {spec.prefix}\n\n"
        "Either shorten the install tree by setting a shorter 'config:install_tree:root',"
        " or enable 8.3 short filename creation on this volume by running"
        " 'fsutil 8dot3name set 0' from an elevated prompt (this only affects files"
        " created afterward, so the package must be reinstalled either way).",
    )


def relocate_win_rpath(spec):
    """Relocates Windows binaries from the stage to the install prefix

    When built with the Windows compiler wrappers, all dll references in
    binaries are absolute paths to the dll location in the stage.
    We need to re-map these to point at the dll's location in the install
    tree so the references make sense at runtime.

    import libraries and the dlls they define are only associated by
    a "dll name" which is impossible to directly resolve after the
    dll has been moved to the install tree. Instead we read a resource entry
    the compiler wrapper injects into all dlls so we can obtain the association
    between a dll's stage location and its install tree location, and remap the
    correct dll for the correct import library.
    """
    dlls = fs.find(spec.prefix, "*.dll")
    exes = fs.find(spec.prefix, "*.exe")
    libs = fs.find(spec.prefix, "*.lib")
    pes = dlls + exes
    targets = pes + libs
    pe_stage_to_prefix = {}
    # map all PE (dll,exe) prefix locations to the stage
    for pe in pes:
        # we don't want to update the rpath to symlinked files
        if fs.islink(pe):
            continue
        # location of PE file at link time (in stage)
        # is baked into PE file as a resource
        # extract it
        stage_pe_loc = extract_spack_id_from_win_pe(pe)
        if stage_pe_loc:
            norm_stage_pe_loc = os.path.normpath(stage_pe_loc)
            pe_stage_to_prefix[norm_stage_pe_loc] = pe
    relocate_windows_binaries(targets, spec, pe_stage_to_prefix, stage=True)


def relocate_windows_binaries(
    targets,
    spec: spack.spec.Spec,
    prefixes: Dict[str, str],
    sfn_prefixes: Optional[Dict[str, str]] = None,
    stage: Optional[bool] = False,
):
    """Relocate Windows PE binaries based on the mappings of "prefixes" and "sfn_prefixes"
    "prefixes" and "sfn_prefixes" provide mappings from one tree to another. This method
    parses the Windows binaries via the relocate feature of the compiler wrapper and
    remaps any dll references.
    """
    pe_targets = [t for t in targets if t.lower().endswith((".dll", ".exe"))]
    # Import libraries may reference their DLL by an 8.3 short filename (SFN) if the
    # build host truncated the path. We can't expand such a path back to its long
    # form here, since the old prefix no longer exists on this host, so instead we
    # also match directly against the SFN form of each old prefix.
    all_prefixes = {**prefixes, **(sfn_prefixes or {})}
    if not pe_targets or not all_prefixes:
        tty.debug(f"Nothing to relocate for {spec.name}, skipping PE relocation...")
        return
    _check_wrapper_can_record(pe_targets, spec)
    # Resolving relocate.exe means either querying the spec or bootstrapping the
    # wrapper, so do it once here rather than once per import library.
    reloc_exe = relocate(spec)
    coff_for_target = _import_lib_targets(targets, all_prefixes, reloc_exe=reloc_exe, stage=stage)
    relocate_pe(all_prefixes, pe_targets, coff_for_target, spec, reloc_exe=reloc_exe)


def relocate_pe(
    prefix_mapping,
    pe_targets,
    coff_mapping,
    spec,
    reloc_exe: Optional[executable.Executable] = None,
):
    if reloc_exe is None:
        reloc_exe = relocate(spec)
    ev = EnvironmentModifications()
    # The wrapper splits this on os.pathsep and then on "|", and strips any padding
    # from both halves of each pair, so the paths we hand it must be unpadded.
    ev.set_path("SPACK_RELOCATE_PATH", ["|".join((k, v)) for k, v in prefix_mapping.items()])
    ev.set("SPACK_INSTALL_PREFIX", spack.store.STORE.layout.root)
    ev.set("SPACK_DEBUG_WRAPPER", "ON")
    apply_pe_relocations(pe_targets, coff_mapping, reloc_exe, ev, fail_on_error=True)


def extract_spack_id_from_win_pe(lib: str) -> Optional[str]:
    """Extracts the string ID spack of type spackresource from the
    string table in a given dll

    The value the compiler wrapper stores here is the absolute path of the PE file at
    link time, padded out to the wrapper's fixed name width with path separators.
    It is returned as-is; ``os.path.normpath`` collapses the padding.

    Arguments:
        lib: the dll to extract the string resource from
    Returns the resource of type SPACKRESOURCE with id spack, or None if the file
    cannot be loaded or carries no such resource.
    """
    if not sys.platform == "win32":
        return None
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    LOAD_LIBRARY_AS_DATAFILE = 0x00000002
    kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
    kernel32.LoadLibraryExW.argtypes = [
        ctypes.wintypes.LPCWSTR,
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.DWORD,
    ]

    kernel32.FreeLibrary.restype = ctypes.wintypes.BOOL
    kernel32.FreeLibrary.argtypes = [ctypes.wintypes.HMODULE]

    kernel32.FindResourceW.restype = ctypes.wintypes.HRSRC
    kernel32.FindResourceW.argtypes = [
        ctypes.wintypes.HMODULE,
        ctypes.wintypes.LPCWSTR,
        ctypes.wintypes.LPCWSTR,
    ]

    kernel32.LoadResource.restype = ctypes.wintypes.HGLOBAL
    kernel32.LoadResource.argtypes = [ctypes.wintypes.HMODULE, ctypes.wintypes.HRSRC]

    kernel32.LockResource.restype = ctypes.wintypes.LPVOID
    kernel32.LockResource.argtypes = [ctypes.wintypes.HGLOBAL]

    kernel32.SizeofResource.restype = ctypes.wintypes.DWORD
    kernel32.SizeofResource.argtypes = [ctypes.wintypes.HMODULE, ctypes.wintypes.HRSRC]

    RESOURCE_ID = "spack"
    RESOURCE_TYPE = "SPACKRESOURCE"
    module_handle = kernel32.LoadLibraryExW(lib, None, LOAD_LIBRARY_AS_DATAFILE)
    if not module_handle:
        # nothing to free, LoadLibraryExW handed back a null handle
        tty.debug(f"Unable to acquire handle for {lib}: {ctypes.get_last_error()}")
        return None

    try:
        res_info_handle = kernel32.FindResourceW(module_handle, RESOURCE_ID, RESOURCE_TYPE)
        if not res_info_handle:
            tty.debug(
                f"Unable to acquire resource info handle for \
{lib}:{RESOURCE_ID}:{RESOURCE_TYPE}: {ctypes.get_last_error()}"
            )
            return None

        resource_data_handle = kernel32.LoadResource(module_handle, res_info_handle)
        if not resource_data_handle:
            tty.debug(
                f"Unable to acquire resource {res_info_handle} \
handle for {lib}: {ctypes.get_last_error()}"
            )
            return None

        data_pointer = kernel32.LockResource(resource_data_handle)
        if not data_pointer:
            tty.debug(f"Unable to lock resource data for {lib}: {ctypes.get_last_error()}")
            return None

        res_size = kernel32.SizeofResource(module_handle, res_info_handle)
        if not res_size:
            tty.debug(
                "Unexpected lack of resource file in Spack based dll, something may be corrupted"
            )
            return None

        raw_id_data = ctypes.string_at(data_pointer, res_size)
    finally:
        kernel32.FreeLibrary(module_handle)

    try:
        # strip null terminator
        return raw_id_data.decode(encoding="utf-8").strip("\x00")
    except UnicodeDecodeError:
        tty.debug(f"Spack resource in {lib} is not valid utf-8, ignoring it")
        return None


def get_importlib_target(
    lib, spec=None, reloc_exe: Optional[executable.Executable] = None
) -> Optional[str]:
    """Extract and return the dll corresponding to the given import library.
    Drives the windows compiler wrapper to obtain the DLL for which the given import
    library provides the linker interface for.

    The returned path is exactly as the wrapper reports it: an absolute Windows path
    padded out to the wrapper's fixed name width. Callers that need to compare it
    against real paths should ``os.path.normpath`` it first.
    """
    if reloc_exe is None:
        reloc_exe = relocate(spec)
    info = reloc_exe("--coff", lib, "--report", output=str)
    if not info:
        # An archive with no longnames member reports nothing and still exits 0
        return None
    regex = re.compile("DLL: (.*)")
    match = regex.search(info)
    if match:
        pe_name = match.group(1).strip("\r")
        return pe_name
    return None


def verify_import_lib(
    lib: str, spec=None, reloc_exe: Optional[executable.Executable] = None
) -> bool:
    """Verifies that a given binary is a windows import library
    using the Windows compiler-wrappers 'relocate' feature
    Behind the scenes, the binary does some basic inspection of the
    structure of the library file provided and discriminates between
    import library coff files and true archive coff files. Supports
    long and short import library formats.

    The wrapper exits 0 for an import library, 1 for a valid archive that is a static
    library rather than an import library, and 2 for something it cannot parse.
    Only 0 is a valid return in this case.
    """
    if reloc_exe is None:
        reloc_exe = relocate(spec)
    out = ""
    try:
        out = reloc_exe("--coff", lib, "--verify", output=str, error=str, ignore_errors=[1])
    except executable.ProcessError:
        tty.debug(f"Cannot verify library {lib} as COFF. Failed with output {out}")
        return False
    return reloc_exe.returncode == 0


def _macho_find_paths(orig_rpaths, deps, idpath, prefix_to_prefix):
    """
    Inputs
    original rpaths from mach-o binaries
    dependency libraries for mach-o binaries
    id path of mach-o libraries
    old install directory layout root
    prefix_to_prefix dictionary which maps prefixes in the old directory layout
    to directories in the new directory layout
    Output
    paths_to_paths dictionary which maps all of the old paths to new paths
    """
    paths_to_paths = dict()
    # Sort from longest path to shortest, to ensure we try /foo/bar/baz before /foo/bar
    prefix_iteration_order = sorted(prefix_to_prefix, key=len, reverse=True)
    for orig_rpath in orig_rpaths:
        for old_prefix in prefix_iteration_order:
            new_prefix = prefix_to_prefix[old_prefix]
            if orig_rpath.startswith(old_prefix):
                new_rpath = re.sub(re.escape(old_prefix), new_prefix, orig_rpath)
                paths_to_paths[orig_rpath] = new_rpath
                break
        else:
            paths_to_paths[orig_rpath] = orig_rpath

    if idpath:
        for old_prefix in prefix_iteration_order:
            new_prefix = prefix_to_prefix[old_prefix]
            if idpath.startswith(old_prefix):
                paths_to_paths[idpath] = re.sub(re.escape(old_prefix), new_prefix, idpath)
                break

    for dep in deps:
        for old_prefix in prefix_iteration_order:
            new_prefix = prefix_to_prefix[old_prefix]
            if dep.startswith(old_prefix):
                paths_to_paths[dep] = re.sub(re.escape(old_prefix), new_prefix, dep)
                break

        if dep.startswith("@"):
            paths_to_paths[dep] = dep

    return paths_to_paths


def _modify_macho_object(cur_path, rpaths, deps, idpath, paths_to_paths):
    """
    This function is used to make machO buildcaches on macOS by
    replacing old paths with new paths using install_name_tool
    Inputs:
    mach-o binary to be modified
    original rpaths
    original dependency paths
    original id path if a mach-o library
    dictionary mapping paths in old install layout to new install layout
    """
    # avoid error message for libgcc_s
    if "libgcc_" in cur_path:
        return
    args = []

    if idpath:
        new_idpath = paths_to_paths.get(idpath, None)
        if new_idpath and not idpath == new_idpath:
            args += [("-id", new_idpath)]

    for dep in deps:
        new_dep = paths_to_paths.get(dep)
        if new_dep and dep != new_dep:
            args += [("-change", dep, new_dep)]

    new_rpaths = []
    for orig_rpath in rpaths:
        new_rpath = paths_to_paths.get(orig_rpath)
        if new_rpath and not orig_rpath == new_rpath:
            args_to_add = ("-rpath", orig_rpath, new_rpath)
            if args_to_add not in args and new_rpath not in new_rpaths:
                args += [args_to_add]
                new_rpaths.append(new_rpath)

    # Deduplicate and flatten
    args = list(itertools.chain.from_iterable(spack.util.lang.dedupe(args)))
    install_name_tool = executable.Executable("install_name_tool")
    if args:
        with fs.edit_in_place_through_temporary_file(cur_path) as temp_path:
            install_name_tool(*args, temp_path)


def _macholib_get_paths(cur_path):
    """Get rpaths, dependent libraries, and library id of mach-o objects."""
    headers = []
    try:
        headers = spack.vendor.macholib.MachO.MachO(cur_path).headers
    except ValueError:
        pass
    if not headers:
        tty.warn("Failed to read Mach-O headers: {0}".format(cur_path))
        commands = []
    else:
        if len(headers) > 1:
            # Reproduce original behavior of only returning the last mach-O
            # header section
            tty.warn("Encountered fat binary: {0}".format(cur_path))
        if headers[-1].filetype == "dylib_stub":
            tty.warn("File is a stub, not a full library: {0}".format(cur_path))
        commands = headers[-1].commands

    LC_ID_DYLIB = spack.vendor.macholib.mach_o.LC_ID_DYLIB
    LC_LOAD_DYLIB = spack.vendor.macholib.mach_o.LC_LOAD_DYLIB
    LC_RPATH = spack.vendor.macholib.mach_o.LC_RPATH

    ident = None
    rpaths = []
    deps = []
    for load_command, dylib_command, data in commands:
        cmd = load_command.cmd
        if cmd == LC_RPATH:
            rpaths.append(_decode_macho_data(data))
        elif cmd == LC_LOAD_DYLIB:
            deps.append(_decode_macho_data(data))
        elif cmd == LC_ID_DYLIB:
            ident = _decode_macho_data(data)

    return (rpaths, deps, ident)


def _set_elf_rpaths_and_interpreter(
    target: str, rpaths: List[str], interpreter: Optional[str] = None
) -> Optional[str]:
    """Replace the original RPATH of the target with the paths passed as arguments.

    Args:
        target: target executable. Must be an ELF object.
        rpaths: paths to be set in the RPATH
        interpreter: optionally set the interpreter

    Returns:
        A string concatenating the stdout and stderr of the call to ``patchelf`` if it was invoked
    """
    # Join the paths using ':' as a separator
    rpaths_str = ":".join(rpaths)

    try:
        # TODO: error handling is not great here?
        # TODO: revisit the use of --force-rpath as it might be conditional
        # TODO: if we want to support setting RUNPATH from binary packages
        args = ["--force-rpath", "--set-rpath", rpaths_str]
        if interpreter:
            args.extend(["--set-interpreter", interpreter])
        args.append(target)
        return _patchelf()(*args, output=str, error=str)
    except executable.ProcessError as e:
        tty.warn(str(e))
        return None


def relocate_macho_binaries(path_names, prefix_to_prefix):
    """
    Use macholib python package to get the rpaths, dependent libraries
    and library identity for libraries from the MachO object. Modify them
    with the replacement paths queried from the dictionary mapping old layout
    prefixes to hashes and the dictionary mapping hashes to the new layout
    prefixes.
    """

    for path_name in path_names:
        # Corner case where macho object file ended up in the path name list
        if path_name.endswith(".o"):
            continue
        # get the paths in the old prefix
        rpaths, deps, idpath = _macholib_get_paths(path_name)
        # get the mapping of paths in the old prerix to the new prefix
        paths_to_paths = _macho_find_paths(rpaths, deps, idpath, prefix_to_prefix)
        # replace the old paths with new paths
        _modify_macho_object(path_name, rpaths, deps, idpath, paths_to_paths)


def relocate_elf_binaries(binaries: Iterable[str], prefix_to_prefix: Dict[str, str]) -> None:
    """Take a list of binaries, and an ordered prefix to prefix mapping, and update the rpaths
    accordingly."""

    # Transform to binary string
    prefix_to_prefix_bin = {
        k.encode("utf-8"): v.encode("utf-8") for k, v in prefix_to_prefix.items()
    }

    for path in binaries:
        try:
            elf.substitute_rpath_and_pt_interp_in_place_or_raise(path, prefix_to_prefix_bin)
        except elf.ElfCStringUpdatesFailed as e:
            # Fall back to `patchelf --set-rpath ... --set-interpreter ...`
            rpaths = e.rpath.new_value.decode("utf-8").split(":") if e.rpath else []
            interpreter = e.pt_interp.new_value.decode("utf-8") if e.pt_interp else None
            _set_elf_rpaths_and_interpreter(path, rpaths=rpaths, interpreter=interpreter)


def relocate_links(links: Iterable[str], prefix_to_prefix: Dict[str, str]) -> None:
    """Relocate links to a new install prefix."""
    regex = re.compile("|".join(re.escape(p) for p in prefix_to_prefix.keys()))
    for link in links:
        old_target = readlink(link)
        if not os.path.isabs(old_target):
            continue
        match = regex.match(old_target)
        if match is None:
            continue

        new_target = prefix_to_prefix[match.group()] + old_target[match.end() :]
        os.unlink(link)
        symlink(new_target, link)


def relocate_text(files: Iterable[str], prefix_to_prefix: PrefixToPrefix) -> None:
    """Relocate text file from the original installation prefix to the
    new prefix.

    Relocation also affects the the path in Spack's sbang script.

    Args:
        files: Text files to be relocated
        prefix_to_prefix: ordered prefix to prefix mapping
    """
    TextFilePrefixReplacer.from_strings_or_bytes(prefix_to_prefix).apply(files)


def relocate_text_bin(binaries: Iterable[str], prefix_to_prefix: PrefixToPrefix) -> List[str]:
    """Replace null terminated path strings hard-coded into binaries.

    The new install prefix must be shorter than the original one.

    Args:
        binaries: paths to binaries to be relocated
        prefix_to_prefix: ordered prefix to prefix mapping

    Raises:
      spack.relocate_text.BinaryTextReplaceError: when the new path is longer than the old path
    """
    return BinaryFilePrefixReplacer.from_strings_or_bytes(prefix_to_prefix).apply(binaries)


def is_macho_magic(magic: bytes) -> bool:
    return (
        # In order of popularity: 64-bit mach-o le/be, 32-bit mach-o le/be.
        magic.startswith(b"\xcf\xfa\xed\xfe")
        or magic.startswith(b"\xfe\xed\xfa\xcf")
        or magic.startswith(b"\xce\xfa\xed\xfe")
        or magic.startswith(b"\xfe\xed\xfa\xce")
        # universal binaries: 0xcafebabe be (most common?) or 0xbebafeca le (not sure if exists).
        # Here we need to disambiguate mach-o and JVM class files. In mach-o the next 4 bytes are
        # the number of binaries; in JVM class files it's the java version number. We assume there
        # are less than 10 binaries in a universal binary.
        or (magic.startswith(b"\xca\xfe\xba\xbe") and int.from_bytes(magic[4:8], "big") < 10)
        or (magic.startswith(b"\xbe\xba\xfe\xca") and int.from_bytes(magic[4:8], "little") < 10)
    )


def is_elf_magic(magic: bytes) -> bool:
    return magic.startswith(b"\x7fELF")


def is_msvc_magic(f: IO[bytes]) -> bool:
    f.seek(0)
    magic = f.read(8)
    if magic.startswith(b"!<arch>\n"):
        return True
    # sanity check for minimal required size
    # need at least 64 bytes for e_lfanew header
    # which gives us the PE signature
    f.seek(0, 2)
    fsize = f.tell()
    if fsize < 0x40:
        return False
    # wasn't a coff file, check PE
    f.seek(0x3C)
    pe_offset_bytes = f.read(4)
    pe_offset = struct.unpack("<I", pe_offset_bytes)[0]
    if pe_offset > fsize:
        return False
    f.seek(pe_offset)
    is_pe = f.read(4) == b"PE\x00\x00"
    f.seek(0)
    return is_pe


def is_binary(filename: str) -> bool:
    """Returns true iff a file is likely binary"""
    with open(filename, "rb") as f:
        magic = f.read(8)

    return is_macho_magic(magic) or is_elf_magic(magic)


# Memoize this due to repeated calls to libraries in the same directory.
@spack.util.lang.memoized
def _exists_dir(dirname):
    return os.path.isdir(dirname)


def is_macho_binary(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            return is_macho_magic(f.read(4))
    except OSError:
        return False


def fixup_macos_rpath(root, filename):
    """Apply rpath fixups to the given file.

    Args:
        root: absolute path to the parent directory
        filename: relative path to the library or binary

    Returns:
        True if fixups were applied, else False
    """
    abspath = os.path.join(root, filename)

    if not is_macho_binary(abspath):
        return False

    # Get Mach-O header commands
    (rpath_list, deps, id_dylib) = _macholib_get_paths(abspath)

    # Convert rpaths list to (name -> number of occurrences)
    add_rpaths = set()
    del_rpaths = set()
    rpaths = collections.defaultdict(int)
    for rpath in rpath_list:
        rpaths[rpath] += 1

    args = []

    # Check dependencies for non-rpath entries
    spack_root = spack.store.STORE.layout.root
    for name in deps:
        if name.startswith(spack_root):
            tty.debug("Spack-installed dependency for {0}: {1}".format(abspath, name))
            (dirname, basename) = os.path.split(name)
            if dirname != root or dirname in rpaths:
                # Only change the rpath if it's a dependency *or* if the root
                # rpath was already added to the library (this is to prevent
                # GCC or similar getting rpaths when they weren't at all
                # configured)
                args += ["-change", name, "@rpath/" + basename]
                add_rpaths.add(dirname.rstrip("/"))

    # Check for nonexistent rpaths (often added by spack linker overzealousness
    # with both lib/ and lib64/) and duplicate rpaths
    for rpath, count in rpaths.items():
        if rpath.startswith("@loader_path") or rpath.startswith("@executable_path"):
            # Allowable relative paths
            pass
        elif not _exists_dir(rpath):
            tty.debug("Nonexistent rpath in {0}: {1}".format(abspath, rpath))
            del_rpaths.add(rpath)
        elif count > 1:
            # Rpath should only be there once, but it can sometimes be
            # duplicated between Spack's compiler and libtool. If there are
            # more copies of the same one, something is very odd....
            tty_debug = tty.debug if count == 2 else tty.warn
            tty_debug("Rpath appears {0} times in {1}: {2}".format(count, abspath, rpath))
            del_rpaths.add(rpath)

    # Delete bad rpaths
    for rpath in del_rpaths:
        args += ["-delete_rpath", rpath]

    # Add missing rpaths that are not set for deletion
    for rpath in add_rpaths - del_rpaths - set(rpaths):
        args += ["-add_rpath", rpath]

    if not args:
        # No fixes needed
        return False

    with fs.edit_in_place_through_temporary_file(abspath) as temp_path:
        executable.Executable("install_name_tool")(*args, temp_path)
    return True


def fixup_macos_rpaths(spec):
    """Remove duplicate and nonexistent rpaths.

    Some autotools packages write their own ``-rpath`` entries in addition to
    those implicitly added by the Spack compiler wrappers. On Linux these
    duplicate rpaths are eliminated, but on macOS they result in multiple
    entries which makes it harder to adjust with ``install_name_tool
    -delete_rpath``.
    """
    if spec.external or not spec.concrete:
        tty.warn("external/abstract spec cannot be fixed up: {0!s}".format(spec))
        return False

    if "platform=darwin" not in spec:
        raise NotImplementedError("fixup_macos_rpaths requires macOS")

    applied = 0

    libs = frozenset(["lib", "lib64", "libexec", "plugins", "Library", "Frameworks"])
    prefix = spec.prefix

    if not os.path.exists(prefix):
        raise RuntimeError(
            "Could not fix up install prefix spec {0} because it does not exist: {1!s}".format(
                prefix, spec.name
            )
        )

    # Explore the installation prefix of the spec
    for root, dirs, files in os.walk(prefix, topdown=True):
        dirs[:] = set(dirs) & libs
        for name in files:
            try:
                needed_fix = fixup_macos_rpath(root, name)
            except Exception as e:
                tty.warn("Failed to apply library fixups to: {0}/{1}: {2!s}".format(root, name, e))
                needed_fix = False
            if needed_fix:
                applied += 1

    specname = spec.format("{name}{/hash:7}")
    if applied:
        tty.info(
            "Fixed rpaths for {0:d} {1} installed to {2}".format(
                applied, "binary" if applied == 1 else "binaries", specname
            )
        )
    else:
        tty.debug("No rpath fixup needed for " + specname)


class WindowsPathTooLongError(spack.error.SpackError):
    """A PE's absolute path exceeds what the compiler wrapper can record, and the volume
    offers no 8.3 short form to fall back on."""
