# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Install/stage debug sources outside any install prefix, keyed by dag_hash.

Two entry points:

install_debug_artifacts(pkg)
    Called from inside the installer while pkg.stage is still alive.
    Uses DWARF + compile_commands.json to capture exactly the files
    referenced by the built binaries (including build-directory generated
    headers), filtered and copied into the out-of-prefix cache.

stage_source(pkg, force=False)
    On-demand fallback for packages installed without --debug-source.
    Re-fetches pristine source via Stage.steal_source(). Cannot recover
    generated headers/compile_commands.json since those never existed
    in the pristine tarball, and has no DWARF to verify the exact
    comp_dir/name layout, so its gdbinit is best-effort.

GDB path resolution note
-------------------------
GDB resolves a compilation unit's source file as the literal string
concatenation of DW_AT_comp_dir + DW_AT_name (no dedup, no smart
normalization beyond '.'/'..' collapsing). E.g. comp_dir="./build",
name="./src/format.cc" resolves to "./build/./src/format.cc". Since
every comp_dir observed in practice starts with "./build", a single
`set substitute-path ./build <dest_root>` rule works, PROVIDED the
captured file is placed at <dest_root>/<composed path with the leading
"build/" stripped>. This has been verified against both fmt (comp_dir
"./build") and hdf5 (comp_dir "./build/src", producing a doubled
"src/src/H5.c" layout) -- see _dest_rel_for_dwarf_pair().
"""
import hashlib
import http.server
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import tarfile
import tempfile
import threading
import time
from typing import TYPE_CHECKING, Dict, Optional, Set, Tuple, List
from urllib.parse import unquote

import spack.binary_distribution
import spack.builder
import spack.config
from spack.stage import StageComposite
import spack.oci.image as oci_image
import spack.oci.oci as oci
import spack.util.path
import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty as tty

if TYPE_CHECKING:
    import spack.package_base


# ---------------------------------------------------------------------------
# Shared cache-root logic (both entry points use this — never write to prefix)
# ---------------------------------------------------------------------------


def debug_source_root() -> str:
    """Root directory for staged/captured debug sources, keyed by dag_hash.
    Deliberately outside any install prefix or build cache -- content here
    never affects the dag_hash and never ships in a binary-cache tarball."""
    root = spack.config.get("config:debug_source_root", "$user_cache_path/debug-sources")
    return spack.util.path.canonicalize_path(root)


def debug_source_dir(spec) -> str:
    """Takes a concrete Spec, not just a hash string, so we can build a readable name."""
    dirname = f"{spec.name}-{spec.version}-{spec.dag_hash()}"
    return os.path.join(debug_source_root(), dirname)


# ---------------------------------------------------------------------------
# ELF / DWARF inspection
# ---------------------------------------------------------------------------


def _is_elf_with_debug_sections(filepath: str) -> bool:
    ELF_MAGIC = b"\x7fELF"
    AR_MAGIC = b"!<arch>\n"
    try:
        with open(filepath, "rb") as f:
            magic = f.read(8)
            if not (magic.startswith(ELF_MAGIC) or magic.startswith(AR_MAGIC)):
                return False
        result = subprocess.run(
            ["readelf", "--sections", "--wide", filepath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=10,
        )
        return ".debug_info" in result.stdout or ".debug_str" in result.stdout
    except (IOError, OSError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _parse_dwarf_comp_unit_paths(readelf_output: str, pairs: Set[Tuple[str, str]]) -> None:
    """Parse readelf --debug-dump=info output into (comp_dir, name) pairs.

    Deliberately does NOT join comp_dir and name here -- callers need the
    pair intact to reproduce GDB's own resolution (literal concatenation)
    when deciding where to place captured files. See module docstring.

    Collects both attributes per compilation-unit DIE before pairing them,
    since DWARF does not guarantee DW_AT_comp_dir precedes DW_AT_name --
    some compilation units emit them in the opposite order (observed in
    practice: hdf5's H5.c, where DW_AT_name preceded DW_AT_comp_dir). A
    strict sequential two-state parser silently drops such CUs with no
    error. DIE boundaries are detected via DW_TAG_compile_unit, a stable
    DWARF tag name, rather than readelf's own line-numbering/bracket
    syntax, which is more likely to vary across binutils versions."""
    comp_dir = None
    name = None
    in_cu = False

    def flush():
        if comp_dir is not None and name is not None:
            pairs.add((comp_dir, name))

    for line in readelf_output.splitlines():
        line = line.strip()

        if "DW_TAG_compile_unit" in line:
            flush()
            comp_dir = None
            name = None
            in_cu = True
            continue

        if not in_cu:
            continue

        if "DW_AT_comp_dir" in line:
            m = re.search(r"DW_AT_comp_dir\b.*:\s*(.+)$", line)
            if m:
                comp_dir = m.group(1).strip()
        elif "DW_AT_name" in line:
            m = re.search(r"DW_AT_name\b.*:\s*(.+)$", line)
            if m:
                name = m.group(1).strip()

    flush()


def _extract_compilation_unit_paths(pkg: "spack.package_base.PackageBase") -> Set[Tuple[str, str]]:
    """Returns a set of (comp_dir, name) pairs, one per compilation unit,
    across every ELF-with-DWARF file in the package's install prefix."""
    prefix = str(pkg.spec.prefix)
    pairs: Set[Tuple[str, str]] = set()
    for root, _, files in os.walk(prefix):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath) or not _is_elf_with_debug_sections(filepath):
                continue
            try:
                result = subprocess.run(
                    ["readelf", "--debug-dump=info", "--dwarf-depth=1", filepath],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=60,
                )
                _parse_dwarf_comp_unit_paths(result.stdout, pairs)
            except subprocess.TimeoutExpired:
                tty.debug(f"[debuggable] readelf timed out on {filepath}, skipping")
            except FileNotFoundError:
                tty.debug("[debuggable] readelf not found on this system")
                return pairs
            except Exception as e:
                tty.debug(f"[debuggable] readelf failed on {filepath}: {e}")
    return pairs


def _dest_rel_for_dwarf_pair(comp_dir: str, name: str) -> str:
    """Given a (comp_dir, name) pair as GDB would see them, compute the path
    (relative to dest_root) where the captured file must be placed so that
    `set substitute-path ./build <dest_root>` resolves it correctly.

    GDB resolves the source file as comp_dir + "/" + name, literally
    concatenated. Since every comp_dir observed starts with "./build" (this
    is guaranteed by the compiler-wrapper's -ffile-prefix-map injection,
    not by this function), stripping a leading "build/" from the composed,
    normalized path gives the correct cache-relative destination.

    Examples (verified manually against fmt and hdf5):
        ("./build", "./src/format.cc")   -> "src/format.cc"
        ("./build/src", "./src/H5.c")    -> "src/src/H5.c"
    """
    composed = os.path.normpath(os.path.join(comp_dir, name))
    if composed.startswith("build/"):
        return composed[len("build/") :]
    if composed == "build":
        return ""
    # Unexpected shape (e.g. an absolute path, or a comp_dir that isn't
    # under "./build" -- possibly DWARF predating the prefix-map injection,
    # or a genuinely external source). Fall back to the composed path as-is
    # rather than guessing further; this may not resolve via the single
    # substitute-path rule, but it's a safe, inspectable fallback.
    return composed.lstrip("/")


# ---------------------------------------------------------------------------
# Entry point 1: install-time, precise, out-of-prefix
# ---------------------------------------------------------------------------


def install_debug_artifacts(pkg: "spack.package_base.PackageBase") -> None:
    """Capture DWARF-referenced sources + generated headers + compile_commands.json
    into debug_source_dir(spec) — never into pkg.spec.prefix.

    Must be called from inside the installer while pkg.stage is still alive
    (the call must occur before the stage/build directory is torn down)."""
    pkg_id = f"{pkg.spec.name}-{pkg.spec.version}-{pkg.spec.dag_hash()}"
    pre = f"{pkg.spec.name}:"

    dest_root = debug_source_dir(pkg.spec)
    fs.mkdirp(dest_root)

    staging_src = pkg.stage.source_path
    try:
        builder = spack.builder.create(pkg)
        staging_build_dir = getattr(builder, "build_directory", None)
    except Exception:
        staging_build_dir = None

    tty.debug(f"{pre} Extracting compilation unit paths from DWARF...")
    dwarf_pairs = _extract_compilation_unit_paths(pkg)
    tty.debug(f"{pre} DWARF reported {len(dwarf_pairs)} compilation units")

    # Map: real staging file path -> destination path relative to dest_root
    files_to_copy: Dict[str, str] = {}

    for comp_dir, name in dwarf_pairs:
        if os.path.isabs(name):
            staging_file = name
        else:
            stripped = name.lstrip("./")
            staging_file = None
            candidate_src = os.path.join(staging_src, stripped) if staging_src else None
            candidate_build = (
                os.path.join(staging_build_dir, stripped) if staging_build_dir else None
            )
            if candidate_src and os.path.isfile(candidate_src):
                staging_file = candidate_src
            elif candidate_build and os.path.isfile(candidate_build):
                staging_file = candidate_build
            else:
                continue  # file not found in either staging root; skip

        rel = _dest_rel_for_dwarf_pair(comp_dir, name)
        if rel:
            assert staging_file is not None
            files_to_copy[staging_file] = rel

    if not files_to_copy:
        tty.debug(f"{pre} DWARF yielded no files; falling back to compile_commands.json")
        for f in _collect_from_compile_commands(pkg, pre):
            if staging_src and f.startswith(staging_src):
                rel = os.path.relpath(f, staging_src)
            else:
                rel = os.path.basename(f)
            files_to_copy[f] = rel
        if not files_to_copy:
            tty.debug(
                f"[debuggable] {pkg_id}: neither DWARF nor compile_commands.json "
                "produced a source list"
            )

    # Headers aren't compilation-unit roots, so DWARF never surfaces them as
    # (comp_dir, name) pairs on their own -- collect them separately from the
    # staging source tree, relative to staging_src, and merge in.
    _HEADER_EXTENSIONS = {".h", ".hh", ".hpp", ".hxx", ".H", ".inl", ".f90", ".f", ".mod"}
    if staging_src and os.path.isdir(staging_src):
        for _root, _, _fnames in os.walk(staging_src):
            for _fname in _fnames:
                if os.path.splitext(_fname)[1] in _HEADER_EXTENSIONS:
                    _fpath = os.path.join(_root, _fname)
                    if os.path.isfile(_fpath) and _fpath not in files_to_copy:
                        files_to_copy[_fpath] = os.path.relpath(_fpath, staging_src)

    if files_to_copy:
        _install_files_to_cache(files_to_copy, dest_root, pre)

    if staging_build_dir and os.path.isdir(staging_build_dir):
        _install_generated_headers(pkg, dest_root, pre, pkg_id)

    _install_compile_commands(pkg, dest_root, pre)


# ---------------------------------------------------------------------------
# Entry point 2: on-demand fallback (for pre-existing installs)
# ---------------------------------------------------------------------------


def stage_source(pkg, *, force: bool = False) -> str:
    """Re-fetch pristine source for an already-installed spec. Cannot recover
    generated headers or compile_commands.json -- those never existed in the
    upstream tarball -- and has no DWARF to verify the exact comp_dir/name
    layout, so the resulting gdbinit is best-effort and may need manual
    substitute-path adjustment."""
    dest_root = debug_source_dir(pkg.spec)
    src_dest = os.path.join(dest_root, "src")

    if os.path.isdir(src_dest) and not force:
        tty.msg(f"Source already staged for {pkg.name} at {src_dest}")
        return src_dest
    if os.path.isdir(src_dest):
        fs.remove_directory_contents(src_dest)

    fs.mkdirp(dest_root)
    stage = pkg.stage[0] if isinstance(pkg.stage, StageComposite) else pkg.stage
    if not stage.created:
        stage.create()
    if not stage.expanded and not stage.archive_file:
        stage.fetch()
        stage.check()  # steal_source's internal fetch() skips this; do it explicitly
    stage.steal_source(src_dest)
    tty.msg(f"Staged source for {pkg.name} at {src_dest}")

    tty.warn(
        f"{pkg.name}: on-demand staging has no DWARF to confirm the exact "
        "comp_dir/name layout used at build time; the generated gdbinit's "
        "substitute-path may not resolve every file. Prefer "
        "'spack install --debug-source' for reliable results."
    )
    write_gdbinit(pkg.spec, dest_root)
    return src_dest


def split_symbols(pkg, *, force: bool = False) -> str:
    """On-demand fallback: split debug symbols for an already-installed
    package that wasn't installed with --debug-symbols.

    Unlike stage_source(), this needs no original build context -- it
    operates purely on the installed ELF binaries in pkg.spec.prefix,
    so it's safe to run at any point after install, on any machine
    that has the binaries (including buildcache-fetched installs)."""
    dest_root = debug_source_dir(pkg.spec)
    symbols_dir = os.path.join(dest_root, "symbols")

    if os.path.isdir(symbols_dir) and not force:
        tty.msg(f"Symbols already split for {pkg.name} at {symbols_dir}")
        return symbols_dir
    if os.path.isdir(symbols_dir):
        fs.remove_directory_contents(symbols_dir)

    fs.mkdirp(dest_root)
    split_debug_files, bytes_saved = split_debug_symbols(pkg)

    if not split_debug_files:
        tty.warn(f"{pkg.name}: no ELF binaries with debug sections were split")
    else:
        write_gdbinit(pkg.spec, dest_root, split_debug_files, bytes_saved)
        tty.msg(f"Split symbols for {pkg.name} at {symbols_dir}")

    return symbols_dir

# ---------------------------------------------------------------------------
# Shared: GDB command file + helpers
# ---------------------------------------------------------------------------


def write_gdbinit(
        spec,
        dest_root: str,
        split_debug_files: Optional[Dict[str, str]] = None,
        bytes_saved: Optional[int] = None
) -> str:
    """Write a GDB command file. Always includes the substitute-path rule.

    If split_debug_files is given, also emits `set debug-file-directory`
    pointing at the symbols/ cache. GDB auto-loads split debug info from
    there via its build-id note lookup at binary/shared-library load time,
    provided the compiler-wrapper injected --build-id/-Wl,--build-id at
    link time. This is a no-op, not an error, on toolchains that don't
    emit a build-id note (see _get_build_id): debug-file-directory then
    simply finds nothing, so a manual add-symbol-file fallback is always
    included as a comment.

    Always includes the substitute-path rule if source has been captured/
    staged for this spec (checked via the presence of dest_root's captured
    source layout, not just a flag, so this stays correct even if called 
    out of order by different entry points -- stage_source, 
    install_debug_artifacts, or split_symbols).

    bytes_saved, if given, is reported as a comment for reference (see
    split_debug_symbols(), which measures it during the split)."""
    gdbinit_path = os.path.join(dest_root, "gdbinit")
    symbols_dir = os.path.join(dest_root, "symbols")
    
    have_source = _dest_root_has_source(dest_root)
    
    with open(gdbinit_path, "w", encoding="utf-8") as f:
        f.write(f"# Generated by 'spack debug' for {spec.name}@{spec.version}\n")
        f.write(f"# dag_hash: {spec.dag_hash()}\n")

        if have_source:
            f.write(f"set substitute-path ./build {dest_root}\n")
            f.write(f"set substitute-path . {dest_root}\n")
        else:
            f.write(
                "# No source captured yet for this spec -- run "
                "'spack debug stage-source' or reinstall with --debug-source\n"
                "# to enable 'set substitute-path ./build <dest_root>'.\n"
            )

        if split_debug_files:
            f.write(f"set debug-file-directory {symbols_dir}\n")
            f.write("#\n")
            f.write(f"# Debug symbols were split for {len(split_debug_files)} binaries into:\n")
            f.write(f"#   {symbols_dir}/\n")
            if bytes_saved is not None:
                f.write(f"# Prefix size reduced by ~{bytes_saved / (1024 * 1024):.1f} MiB\n")
            f.write("# The debug-file-directory line above auto-loads split symbols via\n")
            f.write("# build-id lookup, if your toolchain emits build-id notes at link time.\n")
            f.write("# If it doesn't, or auto-discovery still doesn't trigger, load manually:\n")
            example_bin, example_debug = sorted(split_debug_files.items())[0]
            f.write(f'#   add-symbol-file "{example_debug}" <load-address>   # for {example_bin}\n')
            f.write("#   (get <load-address> from `info sharedlibrary` after `run`)\n")

        f.write("#\n")
        f.write("# Usage: gdb -x <this file> -ex run --args <your-binary> [args...]\n")
        f.write("#    or: gdb -x <this file> -ex 'file <your-binary>'\n")
        f.write("# A bare positional binary argument (gdb -x <this file> <binary>) can\n")
        f.write("# trigger GDB's debuginfo lookup before this script's settings apply --\n")
        f.write("# use --args/-ex run or -ex file instead.\n")
        f.write("#\n")
        f.write("# Note: 'list <file>:N' may report 'no such file' if GDB recorded the\n")
        f.write("# name with a leading './' -- try 'list ./<file>:N' if that happens.\n")
        f.write("# This does not affect breakpoints, backtraces, or normal debugging,\n")
        f.write("# which resolve source via internal DWARF references, not typed names.\n")
    
    tty.msg(f"Wrote GDB command file: {gdbinit_path}")
    tty.msg(f"Use with: gdb -x {gdbinit_path} -ex run --args <your-binary> [args...]")
    tty.msg(f"Or: gdb -x {gdbinit_path} -ex 'file <your-binary>'")
    return gdbinit_path


def _dest_root_has_source(dest_root: str) -> bool:
    """True if source has been captured into dest_root by either
    install_debug_artifacts() (files copied directly under dest_root,
    following DWARF-derived relative paths) or stage_source() (files
    under dest_root/src/). Checked structurally -- via presence of
    actual captured content -- rather than via a caller-supplied flag,
    so this stays correct regardless of call order between the three
    debug_source.py entry points."""
    src_subdir = os.path.join(dest_root, "src")
    if os.path.isdir(src_subdir) and os.listdir(src_subdir):
        return True
    if not os.path.isdir(dest_root):
        return False
    # install_debug_artifacts() copies files directly under dest_root
    # (not under a src/ subdir) -- treat any non-symbols, non-gdbinit
    # content as evidence of a prior source capture.
    for entry in os.listdir(dest_root):
        if entry in ("symbols", "gdbinit", "src", "compile_commands.json"):
            continue
        return True
    return False



def _collect_from_compile_commands(pkg, pre: str) -> Set[str]:
    try:
        builder = spack.builder.create(pkg)
        build_dir = getattr(builder, "build_directory", None)
        if not build_dir:
            return set()
        cc_path = os.path.join(build_dir, "compile_commands.json")
        if not os.path.isfile(cc_path):
            return set()
        with open(cc_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
        return {
            os.path.abspath(e["file"])
            for e in entries
            if e.get("file") and os.path.isfile(e["file"])
        }
    except (json.JSONDecodeError, KeyError, Exception) as e:
        tty.debug(f"{pre} compile_commands.json read failed: {e}")
        return set()


def _install_files_to_cache(files: Dict[str, str], dest_root: str, pre: str) -> None:
    """Copy each staging file to dest_root/rel, per the pre-computed
    DWARF-derived relative destination in `files`."""
    copied = 0
    for staging_file, rel in sorted(files.items()):
        if not os.path.isfile(staging_file):
            continue
        try:
            dst = os.path.join(dest_root, rel)
            fs.mkdirp(os.path.dirname(dst))
            fs.install(staging_file, dst)
            copied += 1
        except Exception as e:
            tty.debug(f"{pre} Could not copy {staging_file}: {e}")
    if copied:
        tty.msg(f"{pre} Installed {copied} files to {dest_root}")


def _install_generated_headers(pkg, dest_root: str, pre: str, pkg_id: str) -> None:
    """Copy generated headers from the build directory, keyed by their path
    relative to the build directory itself. This is the extension-filter
    fallback for build systems (or files) not already captured via DWARF
    comp_dir/name resolution above."""
    HEADER_EXTENSIONS = {
        ".h",
        ".hh",
        ".hpp",
        ".hxx",
        ".H",
        ".f90",
        ".f",
        ".mod",
        ".pb.h",
        ".pb.cc",
        ".c",
        ".cc",
        ".cpp",
        ".cxx",
    }
    GENERATED_SOURCE_PREFIXES = {"moc_", "ui_", "qrc_"}
    EXCLUDED_DIRECTORY_NAMES = {"CMakeFiles", "Testing", "CTestFiles", ".cmake"}

    try:
        builder = spack.builder.create(pkg)
        build_dir = getattr(builder, "build_directory", None)
        if not build_dir or not os.path.isdir(build_dir):
            return
    except Exception:
        return

    for root, dirs, files in os.walk(build_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORY_NAMES and not d.endswith(".dir")]
        for filename in files:
            _, ext = os.path.splitext(filename)
            is_generated_header = ext in HEADER_EXTENSIONS
            is_generated_source = any(filename.startswith(p) for p in GENERATED_SOURCE_PREFIXES)
            if not (is_generated_header or is_generated_source):
                continue
            src_file = os.path.join(root, filename)
            rel = os.path.relpath(src_file, build_dir)
            dst_file = os.path.join(dest_root, rel)
            try:
                fs.mkdirp(os.path.dirname(dst_file))
                fs.install(src_file, dst_file)
            except Exception as e:
                tty.warn(
                    f"[debuggable] {pkg_id}: could not install generated header {src_file}: {e}"
                )


def _install_compile_commands(pkg, dest_root: str, pre: str) -> None:
    try:
        builder = spack.builder.create(pkg)
        build_dir = getattr(builder, "build_directory", None)
        if not build_dir:
            return
        cc_src = os.path.join(build_dir, "compile_commands.json")
        if not os.path.isfile(cc_src):
            return
        fs.mkdirp(dest_root)
        fs.install(cc_src, os.path.join(dest_root, "compile_commands.json"))
    except Exception as e:
        tty.debug(f"{pre} Could not install compile_commands.json: {e}")


# ---------------------------------------------------------------------------
# Symbol splitting
# ---------------------------------------------------------------------------


def _get_build_id(filepath: str) -> Optional[str]:
    """Extract the hex build-id from .note.gnu.build-id via readelf."""
    try:
        result = subprocess.run(
            ["readelf", "-n", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=10
        )
        m = re.search(r"Build ID:\s*([0-9a-f]+)", result.stdout)
        return m.group(1) if m else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def _is_splittable(filepath: str) -> bool:
    """Only .so/executables are splittable with objcopy -- static archives
    (.a) are ar containers of multiple objects and need a different,
    not-yet-implemented per-member workflow. Skip them here rather than
    fail or silently do nothing useful."""
    return not filepath.endswith(".a")


def _split_one_binary(filepath: str, symbols_dir: str, pre: str) -> Optional[str]:
    """Extract debug info from filepath into symbols_dir, strip debug info
    from filepath in place, and link the two via .gnu_debuglink. Also lays
    out a .build-id/xx/yyyy.debug symlink for debuginfod-style lookup.

    Returns the path to the produced .debug file on success, or None if
    splitting was skipped or failed."""
    if not _is_splittable(filepath):
        tty.debug(f"{pre} Skipping symbol split for archive {filepath} (not yet supported)")
        return None

    size_before = os.path.getsize(filepath)

    build_id = _get_build_id(filepath)
    debug_filename = os.path.basename(filepath) + ".debug"
    debug_path = os.path.join(symbols_dir, debug_filename)
    fs.mkdirp(symbols_dir)

    try:
        subprocess.run(
            ["objcopy", "--only-keep-debug", filepath, debug_path],
            check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=60,
        )
        subprocess.run(
            ["objcopy", "--strip-debug", filepath], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60
        )
        subprocess.run(
            ["objcopy", f"--add-gnu-debuglink={debug_path}", filepath],
            check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=60,
        )
    except FileNotFoundError:
        tty.debug(f"{pre} objcopy not found on this system; skipping symbol splitting")
        return None
    except subprocess.TimeoutExpired:
        tty.debug(f"{pre} objcopy timed out on {filepath}, skipping")
        return None
    except subprocess.CalledProcessError as e:
        tty.warn(f"{pre} objcopy failed on {filepath}: {e.stderr.decode(errors='replace')}")
        return None

    size_after = os.path.getsize(filepath)
    tty.msg(f"{pre} Split debug symbols for {os.path.basename(filepath)} -> {debug_path}")

    if build_id and len(build_id) >= 3:
        _write_build_id_link(symbols_dir, build_id, debug_path)
    elif not build_id:
        tty.debug(f"{pre} No build-id found for {filepath}; skipping build-id symlink")

    return debug_path, size_before, size_after


def _write_build_id_link(symbols_dir: str, build_id: str, debug_path: str) -> None:
    """Lay out symbols_dir/.build-id/xx/yyyy.debug as a symlink to debug_path,
    the layout GDB's built-in build-id lookup and debuginfod tooling expect."""
    subdir = os.path.join(symbols_dir, ".build-id", build_id[:2])
    fs.mkdirp(subdir)
    link_path = os.path.join(subdir, build_id[2:] + ".debug")
    if not os.path.lexists(link_path):
        os.symlink(os.path.relpath(debug_path, subdir), link_path)


def split_debug_symbols(pkg: "spack.package_base.PackageBase") -> Tuple[Dict[str, str], int]:
    """Split debug symbols out of every ELF binary in the package's install
    prefix into debug_source_dir(spec)/symbols/, stripping them from the
    installed binaries. Must be called from inside the installer while the
    binaries still exist (any point after the build phases complete).

    If install_debug_artifacts() is also being called in the same install,
    THIS MUST RUN AFTER IT -- stripping debug sections first would make
    install_debug_artifacts()'s readelf-based DWARF scan find nothing.

    Returns a dict mapping each successfully split binary's original path
    to its produced .debug file path, for write_gdbinit() to reference."""
    pkg_id = f"{pkg.spec.name}-{pkg.spec.version}-{pkg.spec.dag_hash()}"
    pre = f"{pkg.spec.name}:"

    dest_root = debug_source_dir(pkg.spec)
    symbols_dir = os.path.join(dest_root, "symbols")
    prefix = str(pkg.spec.prefix)

    split_debug_files: Dict[str, str] = {}
    total_before = 0
    total_after = 0
    for root, _, files in os.walk(prefix):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath) or not _is_elf_with_debug_sections(filepath):
                continue
            result = _split_one_binary(filepath, symbols_dir, pre)
            if result:
                debug_path, size_before, size_after = result
                split_debug_files[filepath] = debug_path
                total_before += size_before
                total_after += size_after

    if split_debug_files:
        saved = total_before - total_after
        tty.msg(
            f"{pre} Prefix size reduced by {saved / (1024 * 1024):.1f} MiB "
            f"across {len(split_debug_files)} binaries "
            f"({total_before / (1024 * 1024):.1f} MiB -> {total_after / (1024 * 1024):.1f} MiB)"
        )
    else:
        tty.debug(f"[debuggable] {pkg_id}: no ELF binaries with debug sections were split")

    return split_debug_files, total_before - total_after


def _iter_split_binaries(dest_root: str):
    """Yield (build_id, debug_file_path) for every split symbol file
    found under dest_root/symbols/.build-id/xx/yyyy.debug."""
    build_id_dir = os.path.join(dest_root, "symbols", ".build-id")
    if not os.path.isdir(build_id_dir):
        return
    for prefix in sorted(os.listdir(build_id_dir)):
        prefix_path = os.path.join(build_id_dir, prefix)
        if not os.path.isdir(prefix_path):
            continue
        for entry in sorted(os.listdir(prefix_path)):
            if entry.endswith(".debug"):
                build_id = prefix + entry[: -len(".debug")]
                yield build_id, os.path.realpath(os.path.join(prefix_path, entry))


def package_source_tarball(dest_root: str, staging_dir: str) -> Optional[str]:
    """Tar the full captured source tree (everything under dest_root except
    symbols/ and gdbinit) into a single blob-ready file. One tarball per
    package, not per build-id -- a package's multiple binaries typically
    share the same source tree (see hdf5's c++/src, fortran/src, java/src,
    tools/lib, etc., all captured under one dest_root), so tarring once
    and referencing it from every build-id's manifest avoids N redundant
    uploads of the same content."""
    if not _dest_root_has_source(dest_root):
        return None
    tar_path = os.path.join(staging_dir, "source.tar.gz")
    with tarfile.open(tar_path, "w:gz") as tf:
        for entry in sorted(os.listdir(dest_root)):
            if entry in ("symbols", "gdbinit"):
                continue
            tf.add(os.path.join(dest_root, entry), arcname=entry)
    return tar_path


def push_debug_artifacts(
    pkg, target_image: "spack.oci.image.ImageReference", *, push_source: bool, push_symbols: bool
) -> None:
    """Push split debug symbols and/or captured source to an OCI mirror,
    keyed by build-id (not dag_hash), since a future debuginfod-compatible
    adapter resolves /buildid/<BUILDID>/{debuginfo,source} requests purely
    by build-id -- see docs/debuginfod.md.

    One shared source tarball is pushed per package (not per build-id),
    since a package's binaries typically share one source tree; each
    build-id's manifest references that same blob by digest, so OCI's
    content-addressing stores it once regardless of how many build-ids
    reference it.
    """

    dest_root = debug_source_dir(pkg.spec)
    pre = f"{pkg.spec.name}:"

    build_ids = list(_iter_split_binaries(dest_root)) if push_symbols else []
    if push_symbols and not build_ids:
        tty.warn(f"{pre} no split debug symbols found to push")

    with tempfile.TemporaryDirectory(prefix="spack-debug-push-") as staging:
        source_tarball = None
        source_digest = None
        if push_source:
            source_tarball = package_source_tarball(dest_root, staging)
            if source_tarball is None:
                tty.warn(f"{pre} no captured source found to push")
            else:
                with open(source_tarball, "rb") as f:
                    source_digest = oci_image.Digest.from_sha256(
                        hashlib.sha256(f.read()).hexdigest()
                    )
                oci.upload_blob_with_retry(target_image, file=source_tarball, digest=source_digest)

        if not build_ids and not source_digest:
            return  # nothing to push

        for build_id, debug_path in build_ids:
            with open(debug_path, "rb") as f:
                debug_digest = oci_image.Digest.from_sha256(hashlib.sha256(f.read()).hexdigest())
            oci.upload_blob_with_retry(target_image, file=debug_path, digest=debug_digest)

            config = oci_image.default_config(
                architecture=spack.binary_distribution._oci_archspec_to_gooarch(pkg.spec),
                os="linux",
            )
            config_bytes = json.dumps(config, separators=(",", ":")).encode()
            config_digest = oci_image.Digest.from_sha256(hashlib.sha256(config_bytes).hexdigest())
            config_path = os.path.join(staging, f"{build_id}.config.json")
            with open(config_path, "wb") as f:
                f.write(config_bytes)
            oci.upload_blob_with_retry(target_image, file=config_path, digest=config_digest)

            manifest = oci_image.default_manifest()
            manifest["config"] = {
                "mediaType": manifest["config"]["mediaType"],
                "digest": str(config_digest),
                "size": len(config_bytes),
            }
            manifest["layers"] = [
                {
                    "mediaType": "application/x-elf-debug",
                    "digest": str(debug_digest),
                    "size": os.path.getsize(debug_path),
                }
            ]
            if source_digest:
                manifest["layers"].append(
                    {
                        "mediaType": "application/x-tar+gzip",
                        "digest": str(source_digest),
                        "size": os.path.getsize(source_tarball),
                    }
                )
            manifest["annotations"] = {
                "build-id": build_id,
                "spack.pkg": pkg.spec.name,
                "spack.dag_hash": pkg.spec.dag_hash(),
            }

            debug_tag = oci_image.ensure_valid_tag(f"debuginfo-{build_id}")
            debug_ref = target_image.with_tag(debug_tag)
            oci.upload_manifest_with_retry(debug_ref, manifest)
            tty.msg(f"{pre} pushed debuginfo for build-id {build_id} as {debug_ref}")

def _oci_mirrors(mirror: Optional["spack.mirrors.mirror.Mirror"] = None) -> List["spack.mirrors.mirror.Mirror"]:
    """Shared by fetch_debug_artifacts() and serve_debuginfod(): resolve to
    a list of OCI-backed binary mirrors to search, honoring an explicit
    override or falling back to every configured OCI mirror."""
    mirrors = [mirror] if mirror else [
        m for m in spack.mirrors.mirror.MirrorCollection(binary=True).values()
        if oci_image.is_oci_url(m.fetch_url)
    ]
    if not mirrors:
        tty.die("No OCI mirrors configured")
    return mirrors


def fetch_debug_artifacts(spec, *, build_id: Optional[str] = None,
                           mirror: Optional["spack.mirrors.mirror.Mirror"] = None) -> str:
    """Fetch previously-pushed debug source/symbols for spec from a
    configured OCI mirror (or all configured OCI mirrors in order),
    unpacking into the same debug_source_dir(spec) layout local capture
    produces -- so gdbinit/substitute-path/debug-file-directory work
    identically regardless of whether the cache was captured locally
    or fetched.

    If build_id is given, only that build-id is fetched. Otherwise,
    every build-id found on spec's installed ELF binaries is fetched."""

    mirrors = _oci_mirrors(mirror)

    build_ids = [build_id] if build_id else _build_ids_from_installed_binaries(spec)
    if not build_ids:
        tty.warn(f"{spec.name}: no build-ids found on installed binaries")
        return debug_source_dir(spec)

    dest_root = debug_source_dir(spec)
    fs.mkdirp(dest_root)
    fetched_any_source = False
    split_debug_files: Dict[str, str] = {}

    for bid in build_ids:
        for m in mirrors:
            target_image = oci.image_from_mirror(m)
            debug_ref = target_image.with_tag(oci_image.ensure_valid_tag(f"debuginfo-{bid}"))
            try:
                manifest, _ = oci.get_manifest_and_config_with_retry(debug_ref)
            except Exception:
                continue  # not on this mirror, try the next

            for layer in manifest["layers"]:
                digest = oci_image.Digest.from_string(layer["digest"])
                with oci.make_stage(debug_ref.blob_url(digest), digest, keep=True) as stage:
                    stage.fetch()
                    stage.check()
                    stage.cache_local()

                    if layer["mediaType"] == "application/x-elf-debug":
                        symbols_dir = os.path.join(dest_root, "symbols")
                        fs.mkdirp(symbols_dir)
                        debug_dest = os.path.join(symbols_dir, f"{bid}.debug")
                        shutil.copy(stage.save_filename, debug_dest)
                        split_debug_files[bid] = debug_dest
                        _write_build_id_link(symbols_dir, bid, debug_dest)
                    elif layer["mediaType"] == "application/x-tar+gzip":
                        with tarfile.open(stage.save_filename, "r:gz") as tf:
                            tf.extractall(dest_root)
                        fetched_any_source = True
            tty.msg(f"{spec.name}: fetched debuginfo for build-id {bid} from {m.name}")
            break  # found on this mirror, stop trying others for this build-id
        else:
            tty.warn(f"{spec.name}: build-id {bid} not found on any configured OCI mirror")

    if split_debug_files or fetched_any_source:
        write_gdbinit(spec, dest_root, split_debug_files or None)
    return dest_root


def _build_ids_from_installed_binaries(spec) -> List[str]:
    """Extract build-ids from every ELF binary in spec's install prefix,
    by reading .note.gnu.build-id directly -- does not require any local
    debug-source cache to already exist."""
    prefix = str(spec.prefix)
    build_ids = []
    for root, _, files in os.walk(prefix):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath):
                continue
            bid = _get_build_id(filepath)
            if bid:
                build_ids.append(bid)
    return build_ids

def serve_debuginfod(*, host: str = "127.0.0.1", port: int = 8002,
                      mirror: Optional["spack.mirrors.mirror.Mirror"] = None) -> None:
    """Run a local debuginfod-compatible HTTP server, resolving build-id
    requests against configured OCI mirrors via the debuginfo-<build-id>
    tag scheme push_debug_artifacts() writes.

    Per the architecture Wouter Deconinck outlined: OCI is the actual
    storage; this is a thin front end that resolves build-id lookups
    against OCI manifests. Both debuginfo and source are proxied through
    Spack's own authenticated OCI client rather than redirected -- a bare
    302 to a registry blob URL doesn't work against registries requiring
    bearer-token auth (e.g. GHCR, even for public packages, since a
    generic HTTP client like GDB's debuginfod client won't perform the
    registry auth handshake before following the redirect). Debug symbol
    files are typically small enough (tens of KB to low MB) that proxying
    is a non-issue in practice.

    Intended to be started/stopped around an active Spack environment's
    lifetime (spack env activate/deactivate), matching the "local, per-
    environment proxy" deployment model from the architecture discussion --
    not run as a standing service by this function."""

    mirrors = _oci_mirrors(mirror)
    buildid_re = re.compile(r"^/buildid/([0-9a-fA-F]+)/(debuginfo|executable|source)(?:/(.*))?$")

    def find_manifest(build_id: str):
        debug_tag = oci_image.ensure_valid_tag(f"debuginfo-{build_id}")
        for m in mirrors:
            try:
                target_image = oci.image_from_mirror(m)
                ref = target_image.with_tag(debug_tag)
                manifest, _ = oci.get_manifest_and_config_with_retry(ref)
                return manifest, ref
            except Exception:
                continue
        return None

    def layer_by_type(manifest, media_type):
        return next((l for l in manifest.get("layers", []) if l.get("mediaType") == media_type), None)

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *a):
            tty.debug(f"[debuginfod] {self.address_string()} - {fmt % a}")

        def do_GET(self):
            match = buildid_re.match(self.path)
            tty.msg(f"[debuginfod] GET {self.path}")
            if not match:
                self.send_error(404, "not a recognized debuginfod endpoint")
                return
            build_id, kind, source_path = match.groups()

            found = find_manifest(build_id)
            if found is None:
                self.send_error(404, f"no debuginfo for build-id {build_id}")
                return
            manifest, ref = found

            if kind == "debuginfo":
                layer = layer_by_type(manifest, "application/x-elf-debug")
                if layer is None:
                    self.send_error(404, "no debuginfo layer")
                    return
                digest = oci_image.Digest.from_string(layer["digest"])
                try:
                    with oci.make_stage(ref.blob_url(digest), digest, keep=True) as stage:
                        stage.fetch()
                        stage.check()
                        stage.cache_local()
                        with open(stage.save_filename, "rb") as f:
                            content = f.read()
                except Exception as e:
                    self.send_error(502, f"fetch failed: {e}")
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/x-elf-debug")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                
            elif kind == "source":
                if not source_path:
                    self.send_error(400, "source path required")
                    return
                layer = layer_by_type(manifest, "application/x-tar+gzip")
                if layer is None:
                    self.send_error(404, "no source layer")
                    return
                digest = oci_image.Digest.from_string(layer["digest"])
                
                # Normalize the same way _dest_rel_for_dwarf_pair() did when this
                # file was placed into the tarball: strip a leading "build/" (GDB's
                # comp_dir+name resolution routinely produces "./build/..." style
                # paths, but the tarball stores files at their dest_root-relative
                # path with that "build/" prefix already stripped -- see
                # install_debug_artifacts()/package_source_tarball()).
                requested = unquote(source_path)
                requested = os.path.normpath(requested)
                if requested.startswith("build/"):
                    requested = requested[len("build/"):]
                elif requested == "build":
                    requested = ""
                requested = requested.lstrip("/")
                
                try:
                    with oci.make_stage(ref.blob_url(digest), digest, keep=True) as stage:
                        stage.fetch()
                        stage.check()
                        stage.cache_local()
                        with tarfile.open(stage.save_filename, "r:gz") as tf:
                            try:
                                member = tf.getmember(requested)
                            except KeyError:
                                self.send_error(404, f"{source_path} not in archive")
                                return
                            content = tf.extractfile(requested).read()
                except Exception as e:
                    self.send_error(502, f"fetch/extract failed: {e}")
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            else:  # executable
                self.send_error(501, "executable endpoint not yet implemented")

    server = http.server.ThreadingHTTPServer((host, port), Handler)
    tty.msg(f"debuginfod-compatible server listening on http://{host}:{port}")
    tty.msg(f"searching mirrors: {', '.join(m.name for m in mirrors)}")
    tty.msg(f"set DEBUGINFOD_URLS=http://{host}:{port} to use it")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        tty.msg("shutting down")
        server.shutdown()

# ---------------------------------------------------------------------------
# Daemon mode for serve_debuginfod
# ---------------------------------------------------------------------------


def _debuginfod_run_dir() -> str:
    """Directory for debuginfod daemon pidfiles/logs, keyed by host:port
    so multiple instances (different mirrors, different ports) can coexist
    on the same node without clobbering each other's state."""
    run_dir = os.path.join(spack.util.path.canonicalize_path("$user_cache_path"), "debuginfod")
    fs.mkdirp(run_dir)
    return run_dir


def _debuginfod_pidfile(host: str, port: int) -> str:
    return os.path.join(_debuginfod_run_dir(), f"{host}-{port}.pid")


def _debuginfod_logfile(host: str, port: int) -> str:
    return os.path.join(_debuginfod_run_dir(), f"{host}-{port}.log")


def _pid_is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # Process exists but owned by someone else -- still "alive" for our purposes.
        return True


def daemon_status(host: str = "127.0.0.1", port: int = 8002) -> Optional[int]:
    """Return the running daemon's PID for this host:port, or None if not running.
    Cleans up a stale pidfile (process no longer alive) if found."""
    pidfile = _debuginfod_pidfile(host, port)
    if not os.path.isfile(pidfile):
        return None
    try:
        with open(pidfile, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
    except (ValueError, OSError):
        # Corrupt pidfile -- treat as not running, clean it up.
        try:
            os.remove(pidfile)
        except OSError:
            pass
        return None

    if _pid_is_alive(pid):
        return pid

    # Stale pidfile from a crashed/killed process.
    try:
        os.remove(pidfile)
    except OSError:
        pass
    return None


def start_debuginfod_daemon(
    *, host: str = "127.0.0.1", port: int = 8002,
    mirror: Optional["spack.mirrors.mirror.Mirror"] = None
) -> int:
    """Fork serve_debuginfod() into a background process tied to the current
    session. The child self-terminates once the shell session that started
    it exits -- a plain fork() child is NOT killed automatically when its
    parent exits (it's just reparented to init and keeps running as an
    orphan, invisible to the shell's own job-control HUP-on-exit behavior
    since it was never registered as a shell job). Instead, the child
    watches the PID of the shell that invoked 'spack debug serve' and
    self-terminates once that PID is gone, regardless of how the session
    ended (normal exit, SSH drop, crash).

    Refuses to start a second daemon for the same host:port. Probes the
    port with a real bind *before* forking, so a collision is reported
    immediately and loudly in the caller's terminal, rather than forking
    into a doomed child and only discovering the failure via the logfile
    after a timeout.
    """
    existing = daemon_status(host, port)
    if existing is not None:
        tty.die(
            f"debuginfod daemon already running for {host}:{port} (pid {existing}). "
            f"Use 'spack debug serve --stop-daemon --host {host} --port {port}' first."
        )

    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        probe.bind((host, port))
    except OSError as e:
        tty.die(
            f"cannot bind {host}:{port} ({e}). A process not tracked by "
            f"'spack debug serve' may already be using this port -- check "
            f"'ss -ltnp | grep {port}' or 'lsof -i :{port}'."
        )
    finally:
        probe.close()

    pidfile = _debuginfod_pidfile(host, port)
    logfile = _debuginfod_logfile(host, port)

    # Resolve mirrors before forking so misconfiguration fails loudly here,
    # not silently in the child.
    mirrors = _oci_mirrors(mirror)

    # Capture the shell session's PID *before* forking -- this is what the
    # child will watch to know when its session has ended.
    session_pid = os.getppid()

    pid = os.fork()
    if pid > 0:
        # Parent: wait for the child to confirm it bound and wrote the
        # pidfile, then return its PID.
        for _ in range(50):  # ~5s
            status = daemon_status(host, port)
            if status is not None:
                return status
            time.sleep(0.1)
        tty.die(
            f"debuginfod daemon did not report ready within 5s; "
            f"check {logfile} for errors"
        )

    # Child: watch the session that started us and self-terminate once it
    # exits. This runs in a background thread so it doesn't interfere with
    # the HTTP server's own event loop below.
    def _watch_session():
        while True:
            time.sleep(2)
            if not _pid_is_alive(session_pid):
                os.kill(os.getpid(), signal.SIGTERM)
                return

    threading.Thread(target=_watch_session, daemon=True).start()

    log_fd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    devnull_fd = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull_fd, 0)
    os.dup2(log_fd, 1)
    os.dup2(log_fd, 2)
    if devnull_fd > 2:
        os.close(devnull_fd)
    if log_fd > 2:
        os.close(log_fd)

    with open(pidfile, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))

    tty.msg(f"debuginfod daemon starting (pid {os.getpid()}), pidfile {pidfile}, logging to {logfile}")

    try:
        serve_debuginfod(host=host, port=port, mirror=mirror)
    finally:
        try:
            os.remove(pidfile)
        except OSError:
            pass
    os._exit(0)


def stop_debuginfod_daemon(*, host: str = "127.0.0.1", port: int = 8002) -> bool:
    """Stop a running daemon for host:port. Returns True if a process was
    signaled, False if nothing was running (not an error -- stopping an
    already-stopped daemon is a no-op, not a failure)."""

    pid = daemon_status(host, port)
    if pid is None:
        return False

    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return False

    for _ in range(30):  # ~3s grace period
        if not _pid_is_alive(pid):
            break
        time.sleep(0.1)
    else:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    pidfile = _debuginfod_pidfile(host, port)
    if os.path.isfile(pidfile):
        try:
            os.remove(pidfile)
        except OSError:
            pass

    return True
