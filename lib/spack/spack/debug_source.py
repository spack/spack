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

import json
import os
import re
import subprocess
from typing import TYPE_CHECKING, Dict, Optional, Set, Tuple

import spack.builder
import spack.config
import spack.util.filesystem as fs
import spack.util.tty as tty

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
    return spack.config.canonicalize_path(root)


def debug_source_dir(spec) -> str:
    """Takes a concrete Spec, not just a hash string, so we can build a readable name."""
    dirname = f"{spec.name}-{spec.version}-{spec.dag_hash()}"
    return os.path.join(debug_source_root(), dirname)


# ---------------------------------------------------------------------------
# ELF / DWARF inspection
# ---------------------------------------------------------------------------


def _is_elf_with_debug_sections(filepath: str) -> bool:
    ELF_MAGIC = b"\x7fELF"
    try:
        with open(filepath, "rb") as f:
            if f.read(4) != ELF_MAGIC:
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
    if not pkg.stage.created:
        pkg.stage.create()
    if not pkg.stage.expanded and not pkg.stage.archive_file:
        pkg.stage.fetch()
        pkg.stage.check()  # steal_source's internal fetch() skips this; do it explicitly
    pkg.stage.steal_source(src_dest)
    tty.msg(f"Staged source for {pkg.name} at {src_dest}")

    tty.warn(
        f"{pkg.name}: on-demand staging has no DWARF to confirm the exact "
        "comp_dir/name layout used at build time; the generated gdbinit's "
        "substitute-path may not resolve every file. Prefer "
        "'spack install --debug-source' for reliable results."
    )
    write_gdbinit(pkg.spec, dest_root)
    return src_dest


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

    bytes_saved, if given, is reported as a comment for reference (see
    split_debug_symbols(), which measures it during the split)."""
    gdbinit_path = os.path.join(dest_root, "gdbinit")
    symbols_dir = os.path.join(dest_root, "symbols")
    with open(gdbinit_path, "w", encoding="utf-8") as f:
        f.write(f"# Generated by 'spack debug' for {spec.name}@{spec.version}\n")
        f.write(f"# dag_hash: {spec.dag_hash()}\n")
        f.write(f"set substitute-path ./build {dest_root}\n")
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
    tty.msg(f"Wrote GDB command file: {gdbinit_path}")
    tty.msg(f"Use with: gdb -x {gdbinit_path} <your-binary>")
    return gdbinit_path


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
