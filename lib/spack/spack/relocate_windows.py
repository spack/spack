# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Relocation of Windows PE binaries (dlls, exes and import libraries) through the
relocate utility of the Windows compiler wrapper.

This lives apart from :mod:`spack.relocate` because driving the wrapper requires the
run environment of the wrapper spec (:mod:`spack.user_environment`), which depends on
:mod:`spack.build_environment`, which in turn depends on :mod:`spack.relocate`."""

import ctypes
import os
import re
import struct
import sys
from typing import Dict, Iterable, List, Optional

import spack.error
import spack.relocate
import spack.spec
import spack.store
import spack.user_environment
import spack.util.executable as executable
import spack.util.filesystem as fs
from spack.util import tty
from spack.util.environment import EnvironmentModifications

if sys.platform == "win32":
    import ctypes.wintypes


WRAPPER_NAME_LEN = 143


def setup_relocate_run(wrapper_spec) -> executable.Executable:
    """Establishes environment neccesary to run the relocate utility, returns the
    executable with the properly established environment."""
    relocate_exe = executable.Executable(str(wrapper_spec.package.bin_dir() / "relocate.exe"))  # type: ignore
    # get msvc context from wrapper - needed for finding msvc utils during relocate run
    relocate_exe.add_default_envmod(
        spack.user_environment.environment_modifications_for_specs(
            wrapper_spec, set_package_py_globals=False
        )
    )
    return relocate_exe


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
        return spack.relocate.bootstrap_relocate()
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
            # The wrapper pads the DLL path it stores in the import library out to a
            # fixed width with path separators; normpath collapses that padding back
            # into the real path.
            norm_dll_path = os.path.normpath(dll_path) if dll_path else ""
            # The wrapper always records an absolute path, so a bare DLL name (or none)
            # means the library was linked without it.
            if not os.path.dirname(norm_dll_path):
                tty.warn(
                    f"Import lib {lib} was not linked by Spack's compiler wrapper, "
                    "skipping relocation..."
                )
                continue
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
        elif pe_has_exports(pe):
            # The wrapper tags every PE it links, so an untagged PE that others can
            # link against was built without it.
            tty.warn(f"{pe} exports symbols but was not linked by Spack's compiler wrapper")
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


def pe_has_exports(path: str) -> bool:
    """Return whether the PE file at ``path`` has an export table."""
    try:
        with open(path, "rb") as f:
            f.seek(0x3C)
            (pe_offset,) = struct.unpack("<I", f.read(4))
            # The optional header follows the 4 byte signature and 20 byte COFF header.
            optional_header = pe_offset + 24
            f.seek(optional_header)
            (magic,) = struct.unpack("<H", f.read(2))
            # NumberOfRvaAndSizes, then the data directories, the first of which is the
            # export table's (RVA, size). Its offset differs between PE32 and PE32+.
            f.seek(optional_header + (108 if magic == 0x20B else 92))
            num_dirs, _, export_size = struct.unpack("<3I", f.read(12))
    except (OSError, struct.error):
        return False
    return num_dirs > 0 and export_size > 0


class WindowsPathTooLongError(spack.error.SpackError):
    """A PE's absolute path exceeds what the compiler wrapper can record, and the volume
    offers no 8.3 short form to fall back on."""
