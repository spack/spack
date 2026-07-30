# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import itertools
import ctypes
import os
import re
import struct
import sys
from typing import IO, Dict, Iterable, List, Optional

import spack.vendor.macholib.mach_o
import spack.vendor.macholib.MachO

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
    import spack.user_environment

    relocate_exe = Executable(str(wrapper_spec.package.bin_dir() / "relocate.exe"))  # type: ignore
    # get msvc context from wrapper - needed for finding msvc utils during relocate run
    relocate_exe.add_default_envmod(
        spack.user_environment.environment_modifications_for_specs(
            wrapper_spec, set_package_py_globals=False
        )
    )
    return relocate_exe


def bootstrap_relocate() -> executable.Executable:
    import spack.bootstrap as spack_bootstrap

    with spack_bootstrap.ensure_bootstrap_configuration():
        # ensure_msvc_relocate_or_raise() may hand back a bare relocate.exe found
        # via a PATH search, with no MSVC environment attached (see the early
        # return in ensure_executables_in_path_or_raise). relocate.exe needs the
        # vcvars-derived INCLUDE/LIB/PATH to find msvc utils (link.exe, lib.exe,
        # dumpbin.exe, ...), so don't trust its return value: look up the
        # concrete compiler-wrapper spec ourselves and always attach its
        # environment, the same way setup_relocate_run does.
        spack_bootstrap.ensure_msvc_relocate_or_raise()
        wrapper_spec = next(
            iter(spack.store.STORE.db.query_local("compiler-wrapper", installed=True)), None
        )
        if not wrapper_spec:
            raise RuntimeError(
                "Failed to bootstrap the MSVC compiler wrapper: no compiler-wrapper spec "
                "found in the bootstrap store after bootstrapping relocate.exe"
            )
        return setup_relocate_run(wrapper_spec)


def relocate(package=None) -> executable.Executable:
    wrapper_spec = None
    if package:
            try:
                wrapper_spec = package.spec["compiler-wrapper"]
            except KeyError:
                pass
    if not wrapper_spec or not wrapper_spec.installed:
        # Don't have one associated with our package installed
        # fine, pull from local db, the functionality we need is
        # origin agnostic
        # NOTE: this will need updating if we ever introduce breaking changes
        # in our relocate behavior
        wrapper_spec = next(
            iter(spack.store.STORE.db.query_local("compiler-wrapper", installed=True)), None
        )
    if not wrapper_spec:
        # We need to bootstrap
        return bootstrap_relocate()
    return setup_relocate_run(wrapper_spec)


@memoized
def dumpbin(pkg) -> executable.Executable:
    db_bin_dir = os.path.dirname(pkg["msvc"].cc)
    dumpbin = executable.which("dumpbin", path=db_bin_dir, required=True)
    return dumpbin


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
        print(f"relocate args: {args}")
        reloc_exe(*args, extra_env=ev, **reloc_kwargs)


def _win_rpath_import_lib_targets(package, pe_stage_to_prefix: dict) -> Dict[str, str]:
    """Match each import library under the package prefix against the stage
    locations recorded in ``pe_stage_to_prefix`` (extracted from each PE's embedded
    SPACKRESOURCE) and return a mapping from PE path to its associated import
    library path, for use as the ``--coff`` argument when relocating that PE.
    """
    coff_for_target: Dict[str, str] = {}
    for lib in fs.find(package.spec.prefix, "*.lib"):
        print(f"processing lib {lib}")
        if verify_import_lib(lib, package=package):
            # we have an import lib, determine associated DLL
            dll_name = get_importlib_target(lib, package=package)
            if dll_name:
                print(f"dll name: {dll_name}")
                prefix_pe = pe_stage_to_prefix.get(dll_name, None)
                print(f"prefix dll {prefix_pe}")
                if prefix_pe:
                    coff_for_target[prefix_pe] = lib
    return coff_for_target


def relocate_win_rpath(package):
    dlls = fs.find(package.spec.prefix, "*.dll")
    exes = fs.find(package.spec.prefix, "*.exe")
    pes = dlls + exes
    pe_stage_to_prefix = {}
    # map all PE (dll,exe) prefix locations to the stage
    for pe in pes:
        # we don't want to update the rpath to symlinked files
        if fs.islink(pe):
            continue
        print(f"Processing {pe}")
        # location of PE file at link time (in stage)
        # is baked into PE file as a resource
        # extract it
        stage_pe_loc = extract_spack_id_from_win_pe(pe)
        if stage_pe_loc:
            print(f"Discovered stage pe location {stage_pe_loc} for pe {pe}")
            pe_stage_to_prefix[stage_pe_loc] = pe
        else:
            print(f"unable to determine stage pe location for {pe}")

    ev = EnvironmentModifications()
    ev.set_path("SPACK_RELOCATE_PATH", ["|".join((k, v)) for k, v in pe_stage_to_prefix.items()])
    ev.set("SPACK_INSTALL_PREFIX", spack.store.STORE.layout.root)
    ev.set("SPACK_DEBUG_WRAPPER", "ON")
    coff_for_target = _win_rpath_import_lib_targets(package, pe_stage_to_prefix)
    apply_pe_relocations(
        pes, coff_for_target, relocate(package), ev, output=str, error=str, fail_on_error=True
    )


def extract_spack_id_from_win_pe(lib: str) -> Optional[str]:
    """Extracts the string ID spack of type spackresource from the
    string table in a given dll
    Arguments:
        lib: the dll to extract the string resource from
    Returns the resource of type SPACKRESOURCE with id spack
    """
    if not sys.platform == "win32":
        return None
    kernel32 = ctypes.windll.kernel32

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
        tty.debug(f"Unable to acquire handle for {lib}: {ctypes.get_last_error()}")
        kernel32.FreeLibrary(module_handle)
        return None

    res_info_handle = kernel32.FindResourceW(module_handle, RESOURCE_ID, RESOURCE_TYPE)
    if not res_info_handle:
        tty.debug(
            f"Unable to acquire resource info handle for \
{lib}:{RESOURCE_ID}:{RESOURCE_TYPE}: {ctypes.get_last_error()}"
        )
        kernel32.FreeLibrary(module_handle)
        return None

    resource_data_handle = kernel32.LoadResource(module_handle, res_info_handle)
    if not resource_data_handle:
        tty.debug(
            f"Unable to acquire resource {res_info_handle} \
handle for {lib}: {ctypes.get_last_error()}"
        )
        kernel32.FreeLibrary(module_handle)
        return None
    data_pointer = kernel32.LockResource(resource_data_handle)
    res_size = kernel32.SizeofResource(module_handle, res_info_handle)

    raw_id_data = ctypes.string_at(data_pointer, res_size)
    str_id_data = raw_id_data.decode(encoding="utf-8").strip("\x00")  # strip null terminator
    kernel32.FreeLibrary(module_handle)
    return str_id_data if res_size else None


def get_importlib_target(lib, package=None) -> Optional[str]:
    reloc = relocate(package)
    info = reloc("--coff", lib, "--report", output=str)
    regex = re.compile("DLL: (.*)")
    match = regex.search(info)
    if match:
        pe_name = match.group(1).strip("\r")
        return pe_name


def verify_import_lib(lib: str, package=None) -> bool:
    relocate_exe = relocate(package)
    try:
        relocate_exe("--coff", lib, "--verify", ignore_errors=[1])
    except executable.ProcessError:
        tty.debug(f"Cannot verify library {lib} as COFF.")
    return relocate_exe.returncode == 0


def collect_import_exports(pkg, lib):
    db = dumpbin(pkg)
    raw_exports = db("/NOLOGO", "/EXPORTS", lib, output=str).split("\n")
    # first 8 lines are boilerplate and not useful
    raw_exports = raw_exports[8:]
    exports = []
    for export_line in raw_exports:
        if export_line == "  Summary\r":
            # exports end just before this section, terminate
            break
        sanitized_line = export_line.strip("\r").strip(" ")
        # some lines define a mangled symbol and their unmangled
        # method declaration, delinated by a whitespace
        # we only care about the mangled symbol name to
        # match with the PE output
        if " " in sanitized_line:
            sanitized_line = sanitized_line.split(" ")[0]
        if not sanitized_line:
            # there are a couple blank lines, just skip them
            continue
        exports.append(sanitized_line)
    return exports


def _buildcache_import_lib_targets(
    targets: List[str], all_prefixes: Dict[str, str]
) -> Dict[str, str]:
    """Match each import library's referenced DLL against ``all_prefixes`` (old
    prefix -> new prefix, including any SFN forms) and return a mapping from the
    DLL's new absolute path to the import library's new absolute path, for use as
    the ``--coff`` argument when relocating that DLL/exe.
    """
    libs = [t for t in targets if t.endswith(".lib")]
    regex = re.compile("|".join(re.escape(p) for p in all_prefixes.keys()))
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
        if sfs.verify_import_lib(lib):
            dll_path = sfs.get_importlib_target(lib)
            print(f"imp lib target {dll_path}")
            if not dll_path:
                tty.debug(
                    f"Import lib {lib} does not reference a compatible DLL, skipping relocation..."
                )
                continue
            # normalizing the padding (stripping out an arbitrary number of escaped backslashes)
            norm_dll_path = dll_path[:2] + "\\" + dll_path[2:].lstrip("\\")
            match = regex.match(norm_dll_path)
            if match:
                old_root = match.group()
                new_root = all_prefixes[old_root]
                dll_name = os.path.relpath(dll_path, old_root)
                new_dll_path = os.path.join(new_root, dll_name)
                coff_for_target[new_dll_path] = lib
            else:
                tty.debug(
                    f"Import lib: {lib} does not reference a DLL "
                    "in this prefix, skipping relocation..."
                )
    return coff_for_target


def relocate_windows_binaries(
    targets,
    spec: spack.spec.Spec,
    prefixes: Dict[str, str],
    sfn_prefixes: Optional[Dict[str, str]] = None,
):
    # Import libraries may reference their DLL by an 8.3 short filename (SFN) if the
    # build host truncated the path. We can't expand such a path back to its long
    # form here, since the old prefix no longer exists on this host, so instead we
    # also match directly against the SFN form of each old prefix.
    all_prefixes = {**prefixes, **(sfn_prefixes or {})}
    ev = EnvironmentModifications()
    ev.set_path("SPACK_RELOCATE_PATH", ["|".join((k, v)) for k, v in all_prefixes.items()])
    ev.set("SPACK_INSTALL_PREFIX", spack.store.STORE.layout.root)
    ev.set("SPACK_DEBUG_WRAPPER", "ON")
    print(["|".join((k, v)) for k, v in all_prefixes.items()])

    coff_for_target = _buildcache_import_lib_targets(targets, all_prefixes)
    pe_targets = [t for t in targets if t.endswith(".dll") or t.endswith(".exe")]
    apply_pe_relocations(pe_targets, coff_for_target, relocate(spec.package), ev, fail_on_error=True)


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
